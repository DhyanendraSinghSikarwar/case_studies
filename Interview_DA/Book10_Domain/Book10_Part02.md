# Book 10 — Domain Knowledge | Part 2: E-commerce & Quick-commerce 🟢🟡🔴

**Target:** 90 questions | **Actual:** 94 questions
**Scope:** how e-commerce and quick-commerce work (orders, GMV, AOV, conversion, returns, RTO, delivery SLAs, dark stores, catalogue, marketplace sellers, payments), their data tables and domain metrics, plain-words privacy awareness and domain analysis tasks.

### Q1 ⭐⭐⭐ 🟢 How does an online marketplace such as Flipkart or Amazon make money, and how is that different from an inventory-led e-commerce retailer and from a quick-commerce company such as Blinkit, Zepto or Swiggy Instamart?
**Asked at:** commonly asked (no company-specific report found); business-model basics are assumed in e-commerce analyst rounds (prep-site guides, unverified).
**What the interviewer is checking:** Whether you know who owns the stock and who earns what, because that decides which numbers you will analyse.
**Say this in the interview:** "A marketplace earns fees from independent sellers (commission, shipping, ads) and does not own most stock. An inventory-led retailer buys goods and earns the margin between buying and selling price. Quick commerce is often inventory-led or a hybrid (models differ by company and change over time), but it ships from small local warehouses, so it earns margin plus fees and lives on delivery speed."
**Explain simply:**
- **Marketplace:** think of a shopping mall. The platform is the landlord; sellers are the shops. The platform earns a *commission* (a percentage of each sale), fees for shipping and payment handling, and *advertising* income when sellers pay to appear higher in search. Its revenue is a slice, not the full sale price.
- **Inventory-led retailer:** the company buys stock from brands, holds it and sells it. Revenue is the full selling price; profit is selling price minus purchase cost (this gap is the *margin*).
- **Quick commerce (q-commerce):** groceries and daily needs in about 10 to 30 minutes from a *dark store* (a small warehouse closed to walk-in customers, see Q5). Earnings come from product margin, delivery and handling fees, and ads from brands. Models differ by company, so say "usually".
- **Why it matters to you:** on a marketplace you analyse seller behaviour and take rate; in inventory-led you analyse stock and margin; in quick commerce you analyse speed, availability and store-level costs.
- **HR parallel:** a marketplace is like a staffing platform that charges a fee per placement; an inventory-led retailer is like employing the staff directly.
**Likely follow-ups:** 1) *What is GMV?* Gross Merchandise Value: total value of goods ordered, before cancellations and returns; not the company's revenue on a marketplace. 2) *What is take rate?* Platform revenue divided by GMV.
**Common mistakes:** Calling marketplace GMV "revenue"; assuming all quick-commerce players share one model; forgetting that ad income can be a large part of marketplace earnings.

### Q2 ⭐⭐⭐ 🟢 Walk me through the life of an e-commerce order, from the customer pressing "place order" to delivery or return, and name the data you get at each stage.
**Asked at:** commonly asked (no company-specific report found); order-lifecycle questions are common in e-commerce SQL and case rounds (prep-site guides, unverified).
**What the interviewer is checking:** That you can map a business process to timestamps and tables, which is what analysis is built on.
**Say this in the interview:** "An order moves through placed, payment confirmed, packed, shipped, out for delivery and delivered, with returns or cancellations as exits. Each step leaves a status and a timestamp, so I can measure time per stage and where orders drop out."
**Explain simply:**
- **Place order:** order ID, customer, items, price, discount, address, payment method, timestamp.
- **Payment:** success or failure, method (UPI, card, cash on delivery), attempt count. COD is paid only at the door.
- **Seller or store confirms, then pick and pack:** confirmation time, picker, pack time, stock-out flags.
- **Ship:** courier (3PL, a third-party logistics company), tracking number, dispatch scan, hub scans along the route.
- **Out for delivery, then delivered or failed:** delivery attempts, failure reason, delivered time. A failed COD order goes back as an *RTO* (see Q3).
- **After delivery:** return request, pickup, quality check, refund, plus ratings and support tickets.
- **Analyst use:** differences between consecutive timestamps give stage times; counts at each stage give a funnel.
**Likely follow-ups:** 1) *Where do most orders drop?* Check payment, seller confirmation and first delivery attempt. 2) *How do you store this?* Either a status-history table (one row per change) or a snapshot (see Q20).
**Common mistakes:** Treating "order" as a single event; ignoring failed payments and cancelled orders; not asking whether timestamps are in one time zone.

### Q3 ⭐⭐⭐ 🟢 What is the difference between a cancellation, a customer return and an RTO (return to origin) in Indian e-commerce, and why does an analyst track them separately?
**Asked at:** commonly asked (no company-specific report found); vendor KPI pages treat cancellation, return and RTO as separate measures (unverified).
**What the interviewer is checking:** Whether you know that three "lost sale" types have different causes, costs and owners.
**Say this in the interview:** "A cancellation happens before the parcel ships, a return happens after the customer accepted delivery, and an RTO is a parcel that never reaches the customer and comes back to the seller. Causes and costs differ, so lumping them hides what to fix."
**Explain simply:**
- **Cancellation:** order stopped before dispatch, by the customer, seller, system or payment failure. Cost is low (no shipping), but a seller-side cancel hurts customer trust.
- **Customer return:** delivered, then sent back for size, quality, wrong item or change of mind. Costs reverse shipping, quality checking and often resale loss. Owner: catalogue, quality, sizing.
- **RTO:** the courier could not deliver (customer absent, refused, wrong address, COD not accepted). The parcel travels both ways at the company's cost. Owner: logistics and address quality, and COD risk.
- **Why separate:** a high return rate points to product or catalogue issues; high RTO points to address or COD issues; high cancellation points to stock or payment issues. Same "lost sale", three different fixes.
**Likely follow-ups:** 1) *Is an RTO a return?* No: the customer never received it. 2) *Which is costliest?* Usually a return or an RTO; compute per-order cost to be sure (see Q25).
**Common mistakes:** Using "returns" for everything; counting RTO in the customer-return rate; ignoring that definitions vary by company.

### Q4 ⭐⭐⭐ 🟢 What is a SKU, and how is it different from a product, a listing and a seller offer on a marketplace?
**Asked at:** commonly asked (no company-specific report found); catalogue basics appear in e-commerce analyst and catalogue-analyst roles (job postings, unverified).
**What the interviewer is checking:** Whether you count the right "thing" when someone says "number of products".
**Say this in the interview:** "A SKU is the smallest sellable, trackable version of an item, for example one shirt in blue, size M. A product groups the variants; a listing is the page customers see; a seller offer is one seller's price and stock for it."
**Explain simply:**
- **SKU (stock keeping unit):** a unique code for each exact variant. T-shirt X in blue/M and blue/L are two SKUs.
- **Product (or parent item):** the idea of "T-shirt X"; it holds many SKUs.
- **Listing:** the page or entry that shows the product to customers, with title, images and description.
- **Seller offer:** on a marketplace, several sellers can sell the same item; each offer has its own price, stock and delivery promise. The platform picks which offer is shown first (the "buy box").
- **Why it matters:** "10,000 products" might mean 10,000 SKUs or 2,000 products with five variants each. Always confirm the grain (the level of one row) before counting.
**Likely follow-ups:** 1) *How do SKU counts mislead?* Many SKUs may sell nothing; look at active, selling SKUs. 2) *What is a catalogue error?* Wrong category, duplicate listing or bad attributes.
**Common mistakes:** Using SKU, product and listing as synonyms; counting offers as SKUs; averaging across SKUs without weighting by sales.

### Q5 ⭐⭐⭐ 🟢 What is a dark store, and how is it different from a normal supermarket and from a fulfilment centre or warehouse?
**Asked at:** commonly asked (no company-specific report found); dark-store vocabulary is central to quick-commerce analyst prep (prep sites, vendor blogs, unverified).
**What the interviewer is checking:** That you understand the physical model behind quick-commerce data.
**Say this in the interview:** "A dark store is a small neighbourhood warehouse set up only for online orders; customers cannot walk in. It is much closer to customers than a fulfilment centre, which is how 10-minute delivery becomes possible."
**Explain simply:**
- **Supermarket:** open to walk-ins; layout and staff serve shoppers; sales happen at a till.
- **Dark store:** shelves arranged for fast picking, typically a few thousand SKUs, serving a radius of a few kilometres (typical pattern, varies by company); staff are pickers and packers, riders collect parcels.
- **Fulfilment centre (FC) or warehouse:** large site, typically lakhs of items (1 lakh = 100,000), serves a city or region, ships by courier within days; also feeds dark stores.
- **Data difference:** dark stores generate hourly stock, pick time, orders per hour and rider wait data; FCs generate inbound, putaway and dispatch data (see Q34).
- **Analyst's lens:** each dark store is like a mini business with its own rent, staff and sales, so store-level profit and availability matter.
**Likely follow-ups:** 1) *Why small assortments?* Space is limited; wrong choices mean stock-outs. 2) *What drives store success?* Orders per store per day, availability and delivery time.
**Common mistakes:** Calling it just a "small warehouse" with no mention of speed and locality; mixing FC and dark-store metrics.

### Q6 ⭐⭐⭐ 🟢 What does a "10-minute delivery" promise contain, and which time stages (order to pick-complete, pick-complete to rider pick-up, ride, handover) does an analyst measure?
**Asked at:** commonly asked (no company-specific report found); pick time and dispatch time are quick-commerce metrics named in vendor blogs (unverified).
**What the interviewer is checking:** Whether you break one headline promise into measurable stages.
**Say this in the interview:** "The promise is a clock from order placed to handover at the door. I split it into assignment, picking, waiting for a rider, the ride and handover, and find which stage eats the minutes."
**Explain simply:**
- **Order to store acceptance:** system or store takes the order.
- **Order to pick-complete (pick time):** a picker collects items from shelves; slow when items are scattered or out of stock.
- **Pick-complete to rider pick-up (dispatch or wait time):** parcel waits for a rider; long waits mean too few riders.
- **Ride:** distance and traffic; depends on delivery radius.
- **Handover:** finding the address, lift, call to customer.
- **Which number:** companies differ in whether the clock starts at order or at store acceptance and whether it is an average, median or percentage within the promise; state your definition.
- **Tip:** report percentiles, not only averages. A percentile answers "nine in ten orders arrive within X minutes", and also report the share of orders that beat the promise.
**Likely follow-ups:** 1) *Why not use only the average?* A few very late orders hide behind a good average. 2) *Which stage first?* The one with the biggest gap versus its target.
**Common mistakes:** Measuring only the ride; not agreeing when the clock starts; ignoring orders that were cancelled for being late.

### Q7 ⭐⭐⭐ 🟢 Why does cash on delivery (COD) matter so much to an Indian e-commerce analyst, and how does it change the metrics you track?
**Asked at:** commonly asked (no company-specific report found); COD and RTO are recurring Indian e-commerce topics in vendor and press pieces (shares quoted there are unverified and not used here).
**What the interviewer is checking:** Whether you know India-specific behaviour that changes failure rates and costs.
**Say this in the interview:** "COD means the customer pays at the door, so there is no payment before shipping. That makes orders easier to place but more likely to fail, so I always split RTO, cancellations and cost by COD versus prepaid."
**Explain simply:**
- **No upfront commitment:** a customer can refuse or be unreachable at no personal cost, so RTO (see Q3) tends to be higher.
- **Cash handling:** couriers collect cash and remit later; this adds reconciliation work and delay.
- **Metrics to split by payment mode:** conversion, cancellation rate, RTO rate, delivery success, AOV, cost per order, and refunds (COD refunds need bank details).
- **Strategy levers:** COD fees, confirmation calls or messages, restricting COD for risky pincodes, nudging to prepaid. A consumer-affairs probe into extra COD charges was reported in the press (from memory, unverified).
- **Analyst use:** blended averages hide this; a good prepaid rate can mask a poor COD rate.
**Likely follow-ups:** 1) *Why is COD still used?* Trust and limited card/UPI use for some buyers. 2) *How would you cut COD RTO?* See Q25.
**Common mistakes:** Quoting overall RTO without the COD split; assuming COD is simply bad (it brings volume); ignoring that COD customers may differ by region and category.

### Q8 ⭐⭐⭐ 🟢 Which tables would you expect in an e-commerce database (customers, orders, order items, products, payments, shipments, returns), and how do they connect to each other?
**Asked at:** commonly asked (no company-specific report found); e-commerce SQL guides use customer, order and payment schemas (prep sites, unverified).
**What the interviewer is checking:** That you can picture the schema before writing joins.
**Say this in the interview:** "Customers place orders; each order has order items that point to products; payments, shipments and returns attach to the order or the item through IDs. I always confirm the grain of each table first."
**Explain simply:**
- **customers:** one row per customer (`customer_id`, city, signup date).
- **orders:** one row per order (`order_id`, `customer_id`, order date, status, shipping fee, total).
- **order_items:** one row per item in an order (`order_id`, `sku_id`, quantity, price). Joins to orders on `order_id`.
- **products (or SKUs):** one row per SKU (`sku_id`, category, MRP, seller).
- **payments:** one row per payment attempt (`order_id`, method, status), so an order can have several rows.
- **shipments:** one row per parcel (`order_id`, courier, dispatch and delivery time); an order may split into several shipments.
- **returns:** one row per returned item (`order_item_id`, reason, date, refund).
- **Links:** customers 1-to-many orders; orders 1-to-many order_items; products 1-to-many order_items. "Many" sides are where joins can duplicate rows (see Q10).
**Likely follow-ups:** 1) *Primary key?* The ID that is unique in its table. 2) *Foreign key?* An ID that points to another table.
**Common mistakes:** Joining without checking the grain; assuming one payment per order; forgetting split shipments.

### Q9 ⭐⭐⭐ 🟢 What do TAT, ETA, SLA, promise date and cut-off time mean in e-commerce delivery operations, and how are they related?
**Asked at:** commonly asked (no company-specific report found); delivery-time terms appear in logistics and e-commerce operations roles (job postings, unverified).
**What the interviewer is checking:** Vocabulary of delivery performance.
**Say this in the interview:** "TAT is how long a step takes, SLA is the agreed target for it, the promise date is what the customer was told, ETA is the live estimate, and the cut-off is the last time an order can be placed to qualify for the promise."
**Explain simply:**
- **TAT (turnaround time):** actual time a step takes, for example order to dispatch.
- **SLA (service level agreement):** the target, for example "dispatch within 24 hours", set between the platform and sellers or couriers.
- **Promise date:** the date shown to the customer at checkout.
- **ETA (estimated time of arrival):** the updating estimate on the tracking page; it can move.
- **Cut-off time:** order before, say, 2 pm gets same-day dispatch; after, next day.
- **Relation:** promise date = order date + SLA, adjusted by the cut-off. On-time means actual delivery is on or before the promise date (see Q12).
- **HR parallel:** offer letter SLA of 5 days, actual TAT 7 days, breach.
**Likely follow-ups:** 1) *Who sets SLA?* Operations, based on past TAT and cost. 2) *Why compare ETA and actual?* To check ETA accuracy.
**Common mistakes:** Treating ETA and promise date as the same; measuring TAT without stating start and end points; ignoring cut-offs when comparing days.

### Q10 ⭐⭐⭐ 🟡 What is the difference between order-level data and order-item-level data, and how does mixing them give wrong order counts or wrong shipping-fee totals?
Data: order 101 has a shipping fee of ₹40 in the orders table and three rows in the order-items table (₹300, ₹200 and ₹100). If you join the two tables and sum the shipping fee, what total do you get for this one order, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); join duplication is a standard SQL-round trap (unverified).
**What the interviewer is checking:** Whether you understand grain and "fan-out" (a join that repeats rows).
**Say this in the interview:** "The join repeats the order row once per item, so ₹40 is counted three times and you get ₹120. Sum the fee from the orders table alone, or aggregate items first and then join."
**Explain simply:**
- **Order level:** one row per order; fields like shipping fee and order total live here.
- **Order-item level:** one row per item; fields like price and quantity live here.
- **Fan-out:** joining one order row to three item rows gives three rows, each carrying the full ₹40.
- **Same trap for counts:** `COUNT(order_id)` after the join counts items, not orders; use `COUNT(DISTINCT order_id)`.
**Worked example:** shipping fee ₹40 repeated on 3 rows = 40 x 3 = ₹120 (wrong, three times too high). Correct: ₹40. Items total = 300 + 200 + 100 = ₹600.
```sql
-- Wrong: the join repeats the order row once per item
SELECT SUM(o.shipping_fee) FROM orders o JOIN order_items i ON i.order_id = o.order_id;
-- Right: take the fee from the orders table only
SELECT SUM(shipping_fee) FROM orders;
```
Output: wrong query returns 120; right query returns 40. In plain words: sum order-level fields at order level.
**Likely follow-ups:** 1) *Need items and fee together?* Aggregate items per order in a subquery, then join. 2) *Spot it fast?* Compare row counts before and after the join.
**Common mistakes:** Trusting a total that jumped after a join; counting rows as orders; allocating fee evenly without saying so.

### Q11 ⭐⭐⭐ 🟡 Walk through the waterfall from gross GMV to net sales after cancellations, RTO and customer returns, and explain why leadership may still quote the gross number.
Data (one month, ₹ crore): gross GMV 100; cancelled before shipping 8; RTO 6; returned after delivery 12. Calculate net delivered sales and each loss as a share of gross GMV.
**Asked at:** commonly asked (no company-specific report found); GMV-to-net-sales logic appears in KPI pages (unverified).
**What the interviewer is checking:** Whether you can reconcile big headline numbers to real sales.
**Say this in the interview:** "Net delivered sales are 74 crore: 100 minus 8 cancelled, 6 RTO and 12 returned. That is a 26% leakage. Leadership may quote gross because it shows demand and growth, but net is what the customer actually kept."
**Explain simply:**
- **Gross GMV:** value of all orders placed.
- **Cancelled before shipping:** order never left the warehouse.
- **RTO:** shipped but not delivered.
- **Returned after delivery:** delivered but sent back.
- **Why gross still gets quoted:** it is the consistent, timely demand measure; net numbers settle weeks later because returns arrive late.
- **Caution:** recent months look better than they are, since returns have not yet arrived (a data lag).
**Worked example (₹ crore):**
- Net delivered = 100 - 8 - 6 - 12 = **74**.
- Cancelled: 8/100 = **8%**; RTO: 6/100 = **6%**; returned: 12/100 = **12%**; total loss 26/100 = **26%**; net 74%.
- Percentages are shares of gross GMV (not percentage points of each other). Returns are 12/(100-8-6)=13.95% of delivered value (about 14%), a different, larger rate.
**Likely follow-ups:** 1) *Is net sales equal to revenue?* Not on a marketplace; revenue is fees. 2) *Does GMV include tax and shipping?* Definitions differ; state yours.
**Common mistakes:** Using gross for profit conversations; computing return share on gross instead of delivered; ignoring return lag.

### Q12 ⭐⭐⭐ 🟡 How do you calculate the on-time delivery rate, and how does the choice of denominator change the answer?
Data (one week): 10,500 shipments had a promised delivery date in the week; 8,700 were delivered on or before the promised date; 1,300 were delivered late; 500 are still undelivered and past the promised date. Calculate the on-time rate on all due shipments and on delivered shipments only.
**Asked at:** commonly asked (no company-specific report found); on-time delivery is a core logistics KPI (unverified).
**What the interviewer is checking:** That you notice undelivered shipments are late too.
**Say this in the interview:** "On all due shipments it is 8,700 out of 10,500, about 82.9%. On delivered shipments only it is 8,700 out of 10,000, which is 87%. The first is honest; the second hides the 500 stuck parcels."
**Explain simply:**
- **Due shipments:** those whose promise date fell in the week; the right base because every one had a chance to be on time.
- **Delivered-only:** drops parcels that never arrived, which flatters the rate.
- **Check:** 8,700 + 1,300 + 500 = 10,500, so the data is consistent.
**Worked example:**
- All due: 8,700 / 10,500 = 0.8286, **82.9%** (rounded to one decimal).
- Delivered only: 8,700 / (8,700 + 1,300) = 8,700 / 10,000 = **87.0%**.
- Gap: 87.0 - 82.9 = 4.1 percentage points (a difference between two percentages, not 4.1%).
**Likely follow-ups:** 1) *Count by promise date or delivery date?* By promise date; otherwise late parcels fall into later weeks. 2) *Weekday effects?* Compare like-for-like days.
**Common mistakes:** Using delivered shipments only; grouping by delivery week; not stating the definition; mixing percentage points and percent.

### Q13 ⭐⭐⭐ 🟡 What is the return rate, and how does it differ when you measure it by orders, by units and by value?
Data (January): 50,000 orders delivered with 60,000 units worth ₹3 crore. Returned: 6,000 units from 4,500 orders worth ₹40 lakh. Calculate the return rate by orders, by units and by value.
**Asked at:** commonly asked (no company-specific report found); return rate appears in KPI pages with differing definitions (unverified).
**What the interviewer is checking:** That you pick a denominator deliberately.
**Say this in the interview:** "Return rate is returned divided by delivered, but it depends on the unit: 9% by orders, 10% by units and 13.3% by value. Value is higher because expensive items return more."
**Explain simply:**
- **By orders:** share of orders with at least one return; good for customer experience and handling workload.
- **By units:** share of items returned; good for inventory.
- **By value:** share of money returned; good for finance.
- **Why they differ:** one order can return one of three items; high-priced items may return more.
- ₹3 crore = 300 lakh (1 crore = 100 lakh).
**Worked example:**
- Orders: 4,500 / 50,000 = **9.0%**.
- Units: 6,000 / 60,000 = **10.0%**.
- Value: 40 / 300 = 0.1333, **13.3%**.
- Returned average item value = 40 lakh / 6,000 = about ₹667, versus ₹500 across delivered units (₹3 crore / 60,000), so returned items are pricier.
**Likely follow-ups:** 1) *Cohort or period basis?* Returns lag; track by delivery month. 2) *Which for the CEO?* Value; for operations, orders.
**Common mistakes:** Dividing by orders placed instead of delivered; mixing units and orders; comparing different definitions across teams.

### Q14 ⭐⭐⭐ 🟡 How do you tag a customer as new or repeat from an orders table, and what goes wrong with guest checkouts, duplicate accounts and a cancelled first order?
**Asked at:** commonly asked (no company-specific report found); new-versus-repeat SQL appears in e-commerce guides (unverified).
**What the interviewer is checking:** Whether you can use ranking by date and spot identity problems.
**Say this in the interview:** "I rank each customer's valid orders by date; the first is new and later ones are repeat. Then I handle guests, duplicates and cancelled orders explicitly, and state the rule."
**Explain simply:**
- **Rule used here:** the first delivered order makes the customer "new"; any later delivered order is "repeat".
- **Cancelled first order:** if you count it, a customer who never received anything looks acquired; exclude it (or decide the policy).
- **Guest checkouts:** with no login, the same person gets many IDs; match on phone or email, knowing matching is imperfect.
- **Duplicate accounts:** the same person with two accounts looks new twice; this overstates new customers.
- **Be consistent:** the same definition on every dashboard.
```sql
-- keep only delivered orders, then number each customer's orders by date
WITH delivered_orders AS (
  SELECT * FROM orders WHERE order_status = 'delivered'
),
numbered AS (
  SELECT order_id, customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_number
  FROM delivered_orders
)
SELECT order_id, customer_id, order_date,
       CASE WHEN order_number = 1 THEN 'new' ELSE 'repeat' END AS customer_type
FROM numbered;
```
Output on a 5-row sample (customer A cancelled first, then delivered): order 2 (A) new, order 3 (B) new, order 4 (B) repeat, order 5 (C) new. In plain words: A is new on the first delivered order, not the cancelled one.
**Likely follow-ups:** 1) *New per month?* Count customers whose first order falls in the month. 2) *Customers who delete accounts?* Handle under privacy rules.
**Common mistakes:** Counting cancelled orders; using customer ID blindly; computing "new" per month with a monthly window instead of all history.

### Q15 ⭐⭐⭐ 🟡 Which metrics would a marketplace use to judge a seller's performance, and what would you do about a seller with high GMV but poor metrics?
**Asked at:** commonly asked (no company-specific report found); seller metrics appear in marketplace analyst job descriptions (unverified).
**What the interviewer is checking:** Whether you balance sales with quality and act proportionately.
**Say this in the interview:** "I would score sellers on seller-caused cancellations, dispatch on time, on-time delivery, return and complaint rates, ratings and catalogue accuracy. A big seller with poor metrics gets a diagnosis and an improvement plan before any penalty."
**Explain simply:**
- **Fulfilment:** seller cancellation rate, dispatch within SLA (see Q9), stock accuracy.
- **Delivery:** on-time delivery rate (Q12), RTO share.
- **Quality:** return rate by reason (defective, not as described), ratings, complaints.
- **Commercial:** GMV, price competitiveness, share of ad spend.
- **High GMV, poor metrics:** compare against category peers; find the cause (stock, packing, courier mix); share a scorecard and a target with a deadline; reduce search visibility only if no improvement. The platform bears the cost of bad experiences.
**Likely follow-ups:** 1) *Why not just ban?* GMV and selection matter; escalate gradually. 2) *Fair comparison?* Within category and city mix.
**Common mistakes:** Ranking only on GMV; using one blended score without showing components; ignoring small sample sizes.

### Q16 ⭐⭐⭐ 🟡 What is the difference between order fill rate and item fill rate in quick commerce, and why do both matter?
Data (one store, one day): 1,000 orders containing 4,000 items. 3,760 items were delivered; 180 orders had at least one item missing. Calculate the item fill rate and the order fill rate.
**Asked at:** commonly asked (no company-specific report found); fill-rate terms appear in quick-commerce vendor blogs (unverified).
**What the interviewer is checking:** That you see how small item gaps become many unhappy orders.
**Say this in the interview:** "Item fill rate is delivered items over ordered items: 94%. Order fill rate is orders delivered complete over all orders: 82%. Both matter because a missing item spoils the whole order for the customer."
**Explain simply:**
- **Item fill rate:** shows stock health.
- **Order fill rate:** shows customer experience: an order missing one item counts as not filled.
- **Why the gap:** 240 missing items are spread over 180 orders (about 1.3 missing items per affected order).
- Premise check: 240 missing items across 180 orders is consistent.
**Worked example:**
- Item fill rate: 3,760 / 4,000 = **94.0%**.
- Orders filled completely: 1,000 - 180 = 820; order fill rate = 820 / 1,000 = **82.0%**.
- Gap: 94.0 - 82.0 = 12 percentage points.
**Likely follow-ups:** 1) *What causes misses?* Stock-outs, picking errors, damaged items. 2) *Which to target?* Order fill rate for experience; item fill rate to find SKUs.
**Common mistakes:** Reporting only item fill rate; treating partial deliveries as full; not separating customer-cancelled items from stock-outs.

### Q17 ⭐⭐⭐ 🟡 Which data and tables would you need to build a daily dashboard for a dark store manager, and which first cuts would you show?
**Asked at:** commonly asked (no company-specific report found); dashboard-building is a staple of quick-commerce analyst guides (unverified).
**What the interviewer is checking:** Whether you start from the manager's daily decisions, not from the data you happen to have.
**Say this in the interview:** "I would ask what the manager decides each shift: staffing, restocking and escalations. Then I would build a one-page view of orders, speed, stock and people, by hour, compared with the same weekday last week."
**Explain simply:**
- A **dark store** is a small warehouse that only serves online orders, so the manager runs it like a factory floor: pick, pack, hand to rider.
- **Orders and order items:** volume by hour, cancellations, items missing (for fill rate).
- **Order timestamps:** placed, pick-started, pick-complete, rider-assigned, picked-up, delivered. These give the time stages.
- **Inventory snapshots:** hourly stock per SKU, for stock-outs and availability, plus near-expiry stock and wastage.
- **Staff and rider roster:** who was scheduled, who logged in, picker count per hour (like an attendance sheet, which is familiar from HR).
- **Complaints and ratings:** wrong or missing items, late delivery.
**First cuts to show:** (1) orders by hour against staff on shift; (2) average and 90th-percentile pick time and delivery time; (3) on-shelf availability with the top 10 stocked-out SKUs; (4) item and order fill rate; (5) cancellations by reason; (6) pending orders older than a threshold, shown live.
**Data and tables involved:** orders, order_items, order_events (timestamps), inventory_hourly, staff_roster, rider_logins, complaints. Joined by order_id, sku_id and store_id.
**Likely follow-ups:** 1) *Why compare with the same weekday?* Demand has a weekly pattern, so Monday should be compared with Monday. 2) *Why show the 90th percentile?* It is the time within which 9 in 10 orders arrive; averages hide the slow orders that cause complaints.
**Common mistakes:** Showing thirty metrics instead of what the manager can act on today; using only averages; ignoring the staffing view; refreshing daily when the manager needs hourly.

### Q18 ⭐⭐⭐ 🟡 What is on-shelf availability (or stock-out rate) in quick commerce, and how would you measure it from hourly stock snapshots?
Data: a store lists 2,000 SKUs and is snapshotted for 14 hours a day. Total in-stock SKU-hours were 25,200. Calculate the availability, and say why a demand-weighted figure can differ.
**Asked at:** commonly asked (no company-specific report found); availability and fill-rate vocabulary appears in quick-commerce vendor blogs (unverified).
**What the interviewer is checking:** Whether you can turn snapshots into a rate and know that not all SKUs matter equally.
**Say this in the interview:** "Availability is the share of SKU-hours in which an item was in stock. Here that is 25,200 divided by 28,000, which is 90%. Weighting by demand can give a different number because popular items matter more."
**Explain simply:**
- An **SKU** is one distinct sellable item (for example, one brand and pack size of milk).
- A **snapshot** records, every hour, which SKUs have stock above zero.
- Possible SKU-hours = 2,000 SKUs x 14 hours = 28,000. Stock-out rate = 1 minus availability.
- **Demand-weighted availability** gives each SKU a weight equal to how much it sells. If the stocked-out 10% are slow sellers, the weighted figure is higher than 90%; if they are the best sellers (milk, eggs), it is much lower, and customers feel the lower one.
**Worked example:** possible SKU-hours = 2,000 x 14 = 28,000. Availability = 25,200 / 28,000 = 0.90 = 90.0%. Stock-out rate = 10.0%, which is 2,800 SKU-hours (about 200 SKUs out of stock at any given hour on average).
**Likely follow-ups:** 1) *What about hours the store is closed?* Exclude them from the denominator. 2) *Does "in stock" mean any quantity?* Many teams use a minimum, such as at least one sellable unit not reserved for another order; state your definition.
**Common mistakes:** Counting days instead of hours; treating all SKUs as equally important; counting SKUs that are deliberately delisted as stock-outs.

### Q19 ⭐⭐⭐ 🟡 How would you analyse payment failure at checkout, and which payment methods and stages would you compare?
Data (one day, attempts / successes): UPI 70,000 / 63,000; cards 20,000 / 17,000; netbanking 5,000 / 4,000. Calculate the success rate by method and overall, and say why attempts and unique orders are not the same.
**Asked at:** commonly asked (no company-specific report found); payments and checkout analysis appears in e-commerce analyst guides (unverified).
**What the interviewer is checking:** Whether you separate the attempt from the order and look for where in the funnel the failure sits.
**Say this in the interview:** "Success rate is successes divided by attempts: UPI 90%, cards 85%, netbanking 80%, and overall 84,000 out of 95,000, about 88.4%. A customer can retry, so attempts are more than orders."
**Explain simply:**
- **UPI** is India's instant bank-to-bank payment through an app; **netbanking** is logging into your bank's website.
- A failed attempt is not always a lost sale: the customer may retry with another method and succeed.
- **Unique orders** count each customer's basket once. If one customer fails twice and then succeeds, that is 3 attempts, 1 order, and 1 eventual success.
- So also report **order-level payment success**: the share of orders that were eventually paid.
**Worked example:** UPI 63,000/70,000 = 90.0%; cards 17,000/20,000 = 85.0%; netbanking 4,000/5,000 = 80.0%. Overall 84,000/95,000 = 88.4% (rounded to 1 decimal). Failures = 11,000. The gap between UPI and netbanking is 10 percentage points. UPI has the largest share of attempts (73.7%), so improving UPI by even 1 point recovers 700 payments.
**Stages and cuts to compare:** payment page loaded, method chosen, authentication step (OTP or UPI approval), bank response, callback to the platform. Then split by failure reason (bank down, wrong OTP, timeout, insufficient balance), bank, app version, device, time of day and new versus repeat customers.
**Likely follow-ups:** 1) *Is a low rate always the platform's fault?* No: bank downtime and user errors count too, so split by reason code. 2) *How do you size the loss?* Failed attempts that never became an order, times average order value.
**Common mistakes:** Treating attempts as orders; averaging the three method rates (86.7%) instead of weighting by attempts; ignoring retries.

### Q20 ⭐⭐⭐ 🟡 An orders table holds several status rows per order (placed, packed, shipped, delivered). How do you pull the latest status per order, and how is a status-history table different from a snapshot table?
**Asked at:** commonly asked (no company-specific report found); window functions are reported in Swiggy candidate reviews and lead/lag in a Flipkart review (anonymous snippets, unverified).
**What the interviewer is checking:** That you can use a window function to keep one row per order and understand how the table was built.
**Say this in the interview:** "I rank each order's rows by time, newest first, and keep rank 1. A history table keeps every change; a snapshot keeps only the current state."
**Explain simply:**
- A **status-history table** adds a new row on every change. It lets you measure the time between stages, but counting rows overcounts orders.
- A **snapshot table** holds one row per order, overwritten on each change. It is easy to count, but the past is lost, so you cannot ask "what was pending last Tuesday?".
- Some teams store daily snapshots, which gives one row per order per day.
```sql
-- rank each order's status rows from newest to oldest
with ranked_status as (
    select order_id, status, changed_at,
           row_number() over (partition by order_id order by changed_at desc) as recency_rank
    from order_status_history
)
-- keep only the newest row of each order
select order_id, status as latest_status, changed_at
from ranked_status
where recency_rank = 1
order by order_id;
```
Output on a small sample: 101 delivered (2026-11-03 15:00); 102 packed (2026-11-01 13:00); 103 cancelled (2026-11-02 08:30). Each order appears once, with its current status.
**Likely follow-ups:** 1) *What if two rows have the same timestamp?* Add a tie-breaker such as a status sequence number or row id. 2) *Why not use max(changed_at)?* It gives the time but not the status unless you join back.
**Common mistakes:** Counting rows in the history table as orders; sorting by status name instead of time; assuming the highest status code is always latest (a cancelled order can come after a shipped one).

### Q21 ⭐⭐⭐ 🟡 What is a monthly transacting user (MTU) and why do e-commerce and quick-commerce companies prefer it to registered or installed users?
Data: 30 lakh orders in a month from 12 lakh transacting users and 80 lakh registered users. Calculate orders per MTU and the share of registered users who transacted.
**Asked at:** commonly asked (no company-specific report found); MTU is a common user metric in app-based businesses (from memory, unverified); definitions differ by company.
**What the interviewer is checking:** Whether you prefer behaviour (buying) over vanity counts (sign-ups).
**Say this in the interview:** "An MTU is a unique user who placed at least one order in the month. Here that is 30 lakh orders over 12 lakh MTUs, so 2.5 orders per MTU, and 15% of registered users transacted."
**Explain simply:**
- A **registered user** signed up once, perhaps years ago and never bought again. An **installed user** just has the app. Neither shows revenue.
- An MTU shows active buying, so it ties to revenue and frequency.
- Definitions vary: some count only delivered orders, some include cancelled ones. State yours.
- HR parallel: registered users are like everyone ever on the payroll; MTUs are like employees who actually worked this month.
**Worked example:** 30 lakh = 3,000,000 orders; 12 lakh = 1,200,000 MTUs. Orders per MTU = 3,000,000 / 1,200,000 = 2.5. Registered users = 8,000,000, so share transacting = 1.2 / 8 = 15.0%. The other 85% (68 lakh) did not buy this month.
**Likely follow-ups:** 1) *What is a related metric?* Frequency (orders per MTU) and the MTU-to-registered ratio, tracked monthly. 2) *Is a rise in MTUs always good?* Not if it came from heavy discounts that did not bring repeat buyers.
**Common mistakes:** Mixing a monthly numerator with a lifetime denominator without saying so; counting orders as users; counting cancelled orders as transacting.

### Q22 ⭐⭐⭐ 🟡 You are asked to build the daily MIS report for an e-commerce operations team. Which columns, views and ageing buckets would you include for orders received, packed, shipped, delivered and pending?
**Asked at:** commonly asked (no company-specific report found); entry-level e-commerce operations and MIS roles in the internal JD sample list daily reporting in Excel and SQL.
**What the interviewer is checking:** Whether you can design a useful operational report, not just list numbers.
**Say this in the interview:** "I would show a funnel by day, orders received, packed, shipped, delivered, then a pending view with ageing buckets so the team can see which orders are stuck and for how long."
**Explain simply:**
- **MIS** (management information system) report here just means a regular, trusted operational report, usually built in Excel or SQL.
- **Funnel view:** received, packed, shipped, delivered, each as a count and as a share of received, by date, warehouse, courier and payment mode.
- **Pending view:** orders not yet in the next stage, with **ageing** (hours or days since the last status change).
- **Ageing buckets (example choice):** under 24 hours, 24 to 48 hours, 48 to 72 hours, over 72 hours. Pick buckets from the promise time, not at random.
- **Key columns:** order_id, order date, SKU count, warehouse, courier, payment mode, pincode, promised date, current status, last status time, age in hours, delay flag.
**Likely follow-ups:** 1) *How do you avoid double counting?* One row per order in the snapshot, built from the latest status. 2) *What would you flag in red?* Orders past their promise date and anything pending in packed for more than a day.
**Common mistakes:** Giving only totals with no pending list; ageing from order date instead of from the last status change; ignoring cancelled orders, so the stages do not add up to received.

### Q23 ⭐⭐⭐ 🔴 The return rate in women's ethnic wear rose from 18% to 27% in six weeks. Which data cuts would you run to find the cause?
**Asked at:** commonly asked (no company-specific report found); Flipkart candidate reviews report case rounds on customer behaviour (anonymous, unverified).
**What the interviewer is checking:** A structured hunt: confirm, localise, then explain.
**Say this in the interview:** "First I confirm the rise is real and which definition is used. Then I split it by reason, size, brand, seller, price and customer type to find where the 9-point jump sits."
**Explain simply:**
- Confirm: same definition (orders, units or value)? Did the denominator change because a sale shifted timing? Returns lag, so recent weeks look lower, which makes a real rise even larger.
- **Return reason:** "size or fit", "colour different from picture", "quality", "wrong item", "damaged". A jump in one reason points to the cause.
- **Product cuts:** by SKU, brand, seller, price band; one new batch or one seller usually explains much.
- **Size and fit:** returns by size, and by size-chart changes.
- **Customer cuts:** new versus repeat, city tier, payment mode, discount used (a sale may bring bargain buyers who return more).
- **Operations:** warehouse, courier, packaging damage, and delivery delay before the return.
- **Contribution analysis:** how many of the 9 points come from each segment; a "mix effect" (more orders came from a segment that always returns more) differs from a "rate effect" (each segment's own return rate went up).
**Data and tables involved:** orders, order_items, returns (reason, date, condition), products (size, brand, seller), customers, shipments.
**Likely follow-ups:** 1) *If it is seller-specific?* Warn, audit quality and photos, then limit listings. 2) *If it is sale-driven?* Compare with the previous sale's return rate.
**Common mistakes:** Jumping to a cause before checking the definition; ignoring return lag; looking only at totals instead of segments.

### Q24 ⭐⭐⭐ 🔴 Late deliveries in Hyderabad rose from 8% to 15% of shipments. Which data cuts would you use to isolate the cause?
**Asked at:** commonly asked (no company-specific report found); diagnostic case rounds are reported for Flipkart and Swiggy (anonymous, unverified).
**What the interviewer is checking:** That you split the delivery journey into stages and segments instead of guessing.
**Say this in the interview:** "I would check the definition of late, then break the delay down by stage, courier, pincode, warehouse and day, to see whether the rise is spread everywhere or sits in one place."
**Explain simply:**
- **Define late:** delivered after the promise date. Check whether promise dates were shortened or the calculation changed.
- **By stage:** order to dispatch (our warehouse), in transit (courier), last mile (the final leg). A rise in one stage points to the owner.
- **By courier (3PL, third-party logistics provider):** one courier's late share jumping is common.
- **By pincode zone and hub:** new areas, a closed hub or heavy traffic.
- **By time:** which days or weeks; a festival, rain, or a strike matters.
- **By volume:** did shipments surge past capacity?
- **By product or seller:** a bulky category or a new seller dispatching late.
- Check failed attempts: customer absent, wrong address.
**Data and tables involved:** shipments (promise date, dispatch, hub scan, out for delivery, delivered), couriers, pincodes, warehouse, delivery attempts.
**Likely follow-ups:** 1) *How do you prove the cause?* Show that the rise disappears when one segment is removed. 2) *What if all segments rose?* Look for a common cause such as a policy or system change.
**Common mistakes:** Averaging delay days instead of using the late share; changing the denominator; stopping at "Hyderabad" without drilling into pincode and courier.

### Q25 ⭐⭐⭐ 🔴 COD orders show a much higher RTO rate than prepaid orders. Use the data to decide whether a confirmation-call programme is worth running, and say what else you would test.
Data (one month): 40,000 COD orders with 14% RTO; 60,000 prepaid orders with 3% RTO. Each RTO costs ₹90 in forward and reverse shipping. A confirmation call costs ₹5 per COD order and is expected to cut COD RTO to 10%.
**Asked at:** commonly asked (no company-specific report found); COD and RTO are common themes in Indian e-commerce analyst preparation (unverified).
**What the interviewer is checking:** Whether you do the break-even, notice what the calculation leaves out, and propose a test.
**Say this in the interview:** "On shipping cost alone, the programme loses money: it saves about ₹1.44 lakh and costs ₹2 lakh. It only breaks even if COD RTO falls to about 8.4%, so I would target the riskiest orders and run a controlled test."
**Explain simply:**
- **COD** (cash on delivery): the customer pays at the door and can refuse. **RTO** (return to origin) means the parcel comes back undelivered.
- Calls on every COD order cost 40,000 x ₹5 = ₹2,00,000.
- RTO now: 14% x 40,000 = 5,600 parcels. After calls: 10% = 4,000. Saved: 1,600 RTOs x ₹90 = ₹1,44,000.
- Net: ₹1,44,000 minus ₹2,00,000 = a loss of ₹56,000.
**Worked example:** break-even needs saved shipping = ₹2,00,000, which is 2,000,000 / 90 = about 2,222 fewer RTOs, a drop of 5.56 percentage points, so COD RTO must fall from 14% to about 8.4%. Figures are computed on the question's invented numbers and ignore other costs.
**What the calculation leaves out:** the margin on orders that become delivered, damaged or unsellable returned goods, handling, and lost customers. These could tip it in favour of calls, so state them as assumptions, not facts.
**What else to test:** call only high-risk orders (new customers, high-RTO pincodes, high basket value); an A/B test with a holdout group; WhatsApp or SMS confirmation (cheaper); a small prepaid discount; a COD fee; blocking COD for repeat refusers.
**Likely follow-ups:** 1) *How do you measure the 10%?* Randomly call half and compare RTO rates. 2) *Is a lower RTO the only goal?* No; check that cancellations from the call do not wipe out the gain.
**Common mistakes:** Comparing COD and prepaid as if the customers were identical; ignoring the cost of calls; treating the expected 10% as proven.

### Q26 ⭐⭐ 🟢 What are the main fulfilment models in e-commerce: seller-fulfilled, platform-fulfilled (such as Fulfilled by Amazon or Flipkart Assured) and inventory-led, and how do they change the data you see?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know who holds the stock and how that changes what data exists.
**Say this in the interview:** "The models differ by who stores, packs and ships. That decides how complete my data is: platform-fulfilled and inventory-led give detailed warehouse data; seller-fulfilled often gives only a few timestamps."
**Explain simply:**
- **Seller-fulfilled:** the seller keeps stock and ships it. The platform sees order, dispatch and delivery scans, but not stock levels or packing steps.
- **Platform-fulfilled** (such as Fulfilled by Amazon or Flipkart Assured, program details from memory, unverified): the seller sends stock to the platform's warehouse, and the platform packs and ships. The platform sees inventory, pick and pack times, and quality checks.
- **Inventory-led:** the platform buys the goods and sells them itself, so it also holds cost price, margin and stock risk.
- Consequence: delivery promises, return handling and data quality are best controlled in the last two models.
**Likely follow-ups:** 1) *Which model makes late delivery easiest to diagnose?* Platform-fulfilled, because every stage is timestamped. 2) *Why would sellers choose platform-fulfilled?* Faster delivery and better search ranking (commonly claimed, unverified).
**Common mistakes:** Assuming all orders have the same timestamps; mixing seller-fulfilled and platform-fulfilled in one on-time rate without segmenting.

### Q27 ⭐⭐ 🟢 What are forward logistics and reverse logistics, and what do first mile, mid mile, last mile, a courier partner (3PL) and a pincode zone mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic supply-chain vocabulary.
**Say this in the interview:** "Forward logistics takes goods to the customer; reverse logistics brings them back. Delivery has three legs: first mile, mid mile and last mile, and many companies use courier partners for them."
**Explain simply:**
- **Forward logistics:** seller to customer. **Reverse logistics:** customer back to seller or warehouse (returns, refunds, RTOs).
- **First mile:** pickup from the seller to the first hub. **Mid mile:** between hubs or cities, by truck or air. **Last mile:** from the local hub to the doorstep, the most expensive and most variable leg.
- **3PL (third-party logistics provider):** an outside courier company that carries parcels for a fee.
- **Pincode zone:** pincodes grouped by distance (local, regional, national), used to set rates and delivery times.
- Data: scans at each hub, so you can compute time in each leg.
**Likely follow-ups:** 1) *Why is last mile costly?* Many stops, small drops, failed attempts. 2) *Why track reverse logistics?* It adds cost with no new sale, plus quality checks.
**Common mistakes:** Assuming reverse logistics is the same cost as forward; ignoring zone when comparing courier costs.

### Q28 ⭐⭐ 🟢 Which metrics spike during a festive sale such as Big Billion Days or the Great Indian Festival, and how should an analyst compare it with a normal period?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that a sale distorts metrics and can compare fairly.
**Say this in the interview:** "Orders, traffic, discounts, cancellations, late deliveries and later returns all rise. I would compare with the same days in the previous sale, and with a normal week, and split out the pull-forward effect."
**Explain simply:**
- **Rise:** traffic, orders, GMV (gross merchandise value, the total value of goods ordered), discount depth, COD share, payment failures, cancellations, late deliveries, support tickets, and returns weeks later.
- **Fall or dip:** the period before the sale (customers wait) and the weeks after (demand pulled forward).
- **Fair comparison:** previous year's sale, normalised for business growth; or a normal week versus the sale week plus the weeks around it. Compare mix too (more low-price items lowers average order value).
- Watch profit, not just volume: discounts cut margin.
**Likely follow-ups:** 1) *How do you measure pull-forward?* Compare the weeks before and after with a normal baseline. 2) *Why look at returns later?* Return reasons show up one or two weeks after delivery.
**Common mistakes:** Comparing sale week to a normal week and calling the whole difference growth; judging the sale before returns land; using the sale average as the new normal.

### Q29 ⭐⭐ 🟢 Why do platforms charge a delivery fee, handling fee, small-cart fee or minimum order value, and which metrics tell you whether these fees work?
**Asked at:** commonly asked (no company-specific report found); fee design is a common quick-commerce improvement question in prep guides (unverified).
**What the interviewer is checking:** Whether you see fees as a trade-off between revenue and conversion.
**Say this in the interview:** "Fees cover real delivery cost, which is nearly fixed per order, and they push customers toward bigger baskets. I would judge them by order value, orders per user, conversion and contribution margin per order."
**Explain simply:**
- A rider trip costs roughly the same for a 2-item and a 20-item basket, so small baskets lose money.
- A **small-cart fee** or **minimum order value** nudges customers to add items; a **handling fee** covers packing cost.
- Metrics: AOV (average order value), share of orders below the threshold, cart abandonment at the fee step, conversion, repeat rate, contribution margin per order (revenue minus variable costs).
- Test fees through A/B tests, not before-and-after, because other things change.
- Note: fee transparency and hidden-charge rules exist in India (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *What if conversion falls?* Check whether margin per order rose enough to offset it. 2) *Does a fee hurt long-term?* Compare repeat rates.
**Common mistakes:** Judging by fee income alone; ignoring customers who leave; comparing across cities of different incomes.

### Q30 ⭐⭐ 🟢 What are the common reasons for cancellations (customer, seller, system, payment, stock-out), and which reasons would you want to reduce first?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate avoidable from unavoidable causes.
**Say this in the interview:** "I would group cancellations by who caused them. Seller, stock-out, system and payment cancellations are within our control, so those come first; customer changes of mind are hard to avoid."
**Explain simply:**
- **Customer:** changed mind, ordered by mistake, found a cheaper price. Partly unavoidable.
- **Seller:** could not ship, price error, late dispatch. Fixable through seller management.
- **Stock-out:** item not available at pick time; points to inventory sync errors.
- **System:** app or pricing glitch.
- **Payment:** payment failed or timed out.
- Prioritise by volume times cost times how fixable the cause is. A stock-out after the customer has paid also harms trust.
- Track the cancellation rate by reason, by stage (before or after dispatch) and by seller or store.
**Likely follow-ups:** 1) *Which stage costs most?* After dispatch, because shipping is already spent. 2) *How do you validate reasons?* Compare the reason code against actual events; "customer cancelled" is sometimes a seller issue.
**Common mistakes:** Trusting reason codes blindly (a default option gets chosen); lumping all cancellations together; ignoring the stage.

### Q31 ⭐⭐ 🟢 What is serviceability in e-commerce and quick commerce, and how is pincode or geofence coverage data used?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know how the platform decides where it can deliver.
**Say this in the interview:** "Serviceability is whether an address can be delivered to, and how fast. E-commerce usually checks pincodes; quick commerce draws a geofence, a map boundary around each dark store."
**Explain simply:**
- **Pincode serviceability:** a table of pincodes per warehouse or courier with delivery time, whether COD is allowed and whether returns can be picked up.
- **Geofence:** a map area, often a small radius around a dark store, inside which the 10-minute promise holds. Outside it, the app shows "not serviceable".
- Uses: expansion decisions, demand lost because of an unserviceable address (search or app opens from unserviceable areas), choosing where to open stores, and spotting areas where promised times are too tight.
**Likely follow-ups:** 1) *How do you size lost demand?* Count app opens or searches at unserviceable locations. 2) *Why shrink a geofence?* To protect delivery time at peak.
**Common mistakes:** Treating serviceability as yes or no only; ignoring COD or return eligibility by pincode.

### Q32 ⭐⭐ 🟢 How do category economics differ between grocery, fashion, electronics and beauty (AOV, margin, return rate, repeat frequency)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the business behaves differently by category, so one metric target does not fit all.
**Say this in the interview:** "Grocery has small baskets, thin margins and frequent repeat. Electronics has large baskets, thin margins and low repeat. Fashion has high returns, and beauty has better margins and frequent repeat. These are general patterns, not company figures."
**Explain simply:** (typical direction only, from memory, unverified)
- **Grocery:** low AOV, low margin, low returns, very high frequency, which is why delivery fees matter.
- **Fashion:** medium AOV, higher margin, high returns because of size and fit, medium frequency.
- **Electronics:** high AOV, thin margin, low returns but costly when they happen (defects), low frequency.
- **Beauty:** low to medium AOV, higher margin, low to medium returns, good repeat.
- Consequence: judge each category against its own targets, and weigh a return in fashion differently from one in electronics.
**Likely follow-ups:** 1) *Why does mix matter?* Total AOV or margin can move simply because the category mix changed. 2) *Which metric suits grocery?* Frequency and contribution margin per order.
**Common mistakes:** Quoting one company-wide return rate; assuming high AOV means high profit.

### Q33 ⭐⭐ 🟢 What is D2C, and how does a brand's own website differ from a marketplace seller in the data it holds?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand who owns the customer relationship and therefore who owns the data.
**Say this in the interview:** "D2C means direct-to-consumer: the brand sells on its own website or app. It owns the full customer and browsing data. A marketplace seller only sees what the platform chooses to share, usually order-level data."
**Explain simply:**
- **D2C (direct-to-consumer):** the brand skips the middleman, like a company running its own canteen instead of selling through a food court.
- **Own website:** the brand holds customer name, contact details, browsing clicks, cart behaviour, coupon use and repeat purchases, all linked to one customer ID. It also pays for its own ads, payment gateway and delivery.
- **Marketplace seller:** the platform owns the customer. The seller usually gets the order, the delivery address needed to ship, and sales reports, but typically not the full browsing history or a reusable customer profile (what is shared varies by platform).
- **Trade-off:** the marketplace brings ready traffic but less data and less control; the own site gives rich data but the brand must buy traffic and build everything.
**Likely follow-ups:** 1) *Which has better repeat-purchase analysis?* The own site, because customers are identifiable over time. 2) *Can a brand do both?* Yes, many sell on both; compare channels with the same metric definitions.
**Common mistakes:** Assuming a seller can see every customer's history; comparing own-site and marketplace conversion without noting that marketplace traffic arrives with higher buying intent.

### Q34 ⭐⭐ 🟢 What are the main steps inside a fulfilment centre (inbound, putaway, pick, pack, ship), and which data is captured at each step?
**Asked at:** commonly asked (no company-specific report found); fulfilment-centre MIS appears in entry-level operations job descriptions in the internal JD sample.
**What the interviewer is checking:** That you can follow an item through a warehouse and know where timestamps and counts come from.
**Say this in the interview:** "A fulfilment centre receives stock (inbound), stores it in a location (putaway), collects it for an order (pick), boxes it (pack) and hands it to a courier (ship). Each step scans the item, so every step leaves a timestamp, a user and a quantity."
**Explain simply:**
- **Inbound:** goods arrive from the seller or supplier. Data: purchase order or shipment number, expected vs received quantity, damaged units, receiving time.
- **Putaway:** items are placed on a shelf or bin. Data: SKU, bin location, quantity, putaway time, who did it.
- **Pick:** a worker collects the items for an order from bins. Data: pick start and end time, picker ID, short picks (item not found).
- **Pack:** items are checked and boxed. Data: pack time, packer ID, box type and weight, label printed.
- **Ship (dispatch):** parcels are sorted to a courier and handed over. Data: courier, AWB (air waybill, the tracking number), handover time, dispatch SLA met or missed.
- These timestamps give the pending-orders ageing in the MIS: how long each order has been stuck at each stage.
**Likely follow-ups:** 1) *Which step is usually the bottleneck?* Check the time between stages; the longest median gap points to it. 2) *Why track short picks?* They show inventory records that do not match the shelf.
**Common mistakes:** Treating the warehouse as one black box with a single "dispatch" date; ignoring receiving errors that corrupt stock counts later.

### Q35 ⭐⭐ 🟡 A seller sells a ₹1,000 item. Calculate the seller payout and the platform's take rate from the fees below, and say which fees are commonly charged by marketplaces.
Data: commission 12%, fixed closing fee ₹20, shipping fee ₹60, collection fee 2% of price. Ignore GST.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can build a seller payout waterfall and define take rate with a clear numerator.
**Say this in the interview:** "Total fees are ₹220, so the seller payout is ₹780 and the take rate is 22% of the selling price. Because the shipping fee may largely pass through to the courier (varies by platform), the platform's own earning can be lower, so I would state which definition I use."
**Explain simply:**
- **Take rate:** fees collected from sellers divided by the item's selling price (or by GMV, the total value of orders placed). Definitions differ by company.
- **Commission:** a percentage of price for using the marketplace. **Closing fee:** a flat charge per sold item. **Shipping fee:** charge for delivery, often by weight and zone. **Collection fee:** payment-handling charge.
- Marketplaces commonly also charge (from memory, unverified): fees on returns, storage or fulfilment fees, and advertising spend. Which ones apply depends on the platform and category.
**Worked example:** all figures computed, in ₹.
- Commission: 12% x 1,000 = 120
- Collection fee: 2% x 1,000 = 20
- Closing fee 20 + shipping 60
- Total fees: 120 + 20 + 20 + 60 = 220
- Seller payout: 1,000 - 220 = **₹780**
- Take rate including shipping: 220 / 1,000 = **22%**
- Excluding the shipping fee (pass-through to the courier): 160 / 1,000 = **16%**
**Likely follow-ups:** 1) *Does GST change it?* Yes, GST is charged on fees; it is ignored here as instructed. 2) *What if the item is returned?* The seller may lose the payout and still pay some fees, depending on policy.
**Common mistakes:** Applying the percentage fees to the payout instead of the price; mixing shipping (a cost pass-through) into platform revenue without saying so.

### Q36 ⭐⭐ 🟡 What are ROAS and ACoS for sponsored listings on a marketplace, and how do ad revenues fit into platform revenue?
Data: a brand spent ₹50,000 on sponsored listings and the ads were credited with ₹4,00,000 of sales. Calculate ROAS and ACoS.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know both ad ratios, that they are inverses, and that neither is profit.
**Say this in the interview:** "ROAS is 8, meaning ₹8 of ad-attributed sales per ₹1 spent. ACoS is 12.5%, the ad spend as a share of ad sales. They are inverses: 1 divided by 8."
**Explain simply:**
- **Sponsored listing:** a paid ad where a seller pays to appear higher in search results.
- **ROAS (return on ad spend):** ad-attributed sales / ad spend. **ACoS (advertising cost of sales):** ad spend / ad-attributed sales.
- Both use sales, not profit. If the product margin is 20% (invented), break-even ROAS is 1/0.20 = 5, so a ROAS of 8 is profitable before other costs, but 4 would lose money.
- For the platform, ad income is a separate revenue line on top of commissions and fees. It is often high margin, so platforms track it as a share of GMV (percentage figures vary by company; not stated here).
- Attribution matters: ads may be credited with sales that would have happened organically.
**Worked example:** ROAS = 4,00,000 / 50,000 = **8.0**. ACoS = 50,000 / 4,00,000 = **12.5%**.
**Likely follow-ups:** 1) *How do you check true ad impact?* Compare with a holdout (no-ad) group. 2) *Which is better, high or low ACoS?* Lower, subject to margin and growth goals.
**Common mistakes:** Reading ROAS as profit; forgetting that a long attribution window inflates credited sales.

### Q37 ⭐⭐ 🟡 How do you measure on-site search quality, and what is the zero-result or null-search rate?
Data (one day): 2,00,000 searches; 12,000 returned no results; 30,000 searches ended in an order. Calculate the null-search rate and the search-to-order rate.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can pick sensible quality measures for search and compute them with clear denominators.
**Say this in the interview:** "The null-search rate is 6%: 12,000 of 2,00,000 searches found nothing. The search-to-order rate is 15%. I would also look at click-through and the top null queries."
**Explain simply:**
- **Null (zero-result) search:** the customer typed something and saw no products, a lost chance and a clue about missing products or spelling problems.
- **Search-to-order rate:** searches that ended in an order / total searches. Here orders are searches that ended in a purchase, as the data says.
- Other quality signals: click-through rate on results, how often people refine or re-search, and share of searches with a click in the top few results.
- First action: rank the null queries by frequency; each is either a spelling or synonym issue, an item you do not stock, or a language mix (such as Hindi words in English letters).
**Worked example:** null-search rate = 12,000 / 2,00,000 = **6.0%**. Search-to-order = 30,000 / 2,00,000 = **15.0%**. Among searches that did return results (1,88,000), 30,000 / 1,88,000 = 15.96%, about 16.0%, since null searches cannot convert.
**Likely follow-ups:** 1) *Is a low null rate always good?* No; irrelevant results can hide failure. 2) *Which denominator for a user view?* Unique searchers rather than searches, if repeats distort.
**Common mistakes:** Using orders as the denominator; counting repeated retries as separate failures without noting it.

### Q38 ⭐⭐ 🟡 How would you use the 80/20 (Pareto) view on SKUs and categories, and what decisions does it support?
Data: a category has 1,000 SKUs; the top 100 give 62% of GMV and the bottom 500 give 4%. What would you check before you delist the tail?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you use Pareto as a starting point, not as an automatic delisting rule.
**Say this in the interview:** "Rank SKUs by GMV, add a running total and see how few drive most sales. Here 10% of SKUs give 62% and the bottom 50% give just 4%. Before delisting I would check why the tail is small and what it contributes beyond its own sales."
**Explain simply:**
- **Pareto (80/20) view:** sort items from biggest to smallest contributor and look at the cumulative share. It supports assortment decisions, stock allocation, and where to focus effort.
- The middle 400 SKUs give 100 - 62 - 4 = 34% of GMV, so the picture is not only head and tail.
- **Check before delisting:**
  - Age: new SKUs have not had time to sell.
  - Availability: low sales may come from being out of stock, not low demand.
  - Margin: a small SKU may carry high margin.
  - Role: some items are needed for basket completion or bring customers back (for example staples).
  - Fixed cost: delisting frees storage or working capital only if stock is actually removed.
  - Stability: check over several periods, since one month can mislead.
**Worked example:** top 100 of 1,000 = 10% of SKUs for 62% of GMV; bottom 500 = 50% of SKUs for 4% of GMV; middle 400 = 34% of GMV.
**Likely follow-ups:** 1) *Do you do this by GMV only?* No, add margin and units. 2) *How is it useful for categories?* Same view guides which categories get marketing or space.
**Common mistakes:** Cutting the tail without checking stock-outs and new launches; assuming the exact 80/20 split always appears.

### Q39 ⭐⭐ 🟡 What is the difference between MRP, selling price, discount percentage and effective price after bank offers, and why can an average discount mislead?
Data: a phone has an MRP of ₹20,000 and a selling price of ₹15,000, plus a ₹1,000 bank offer. Calculate the headline discount and the effective discount.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute discounts correctly and spot averaging traps.
**Say this in the interview:** "The headline discount is 25% off MRP. After the ₹1,000 bank offer the effective price is ₹14,000, a 30% effective discount, but only for customers who use that card."
**Explain simply:**
- **MRP (maximum retail price):** the printed top price. **Selling price:** the price shown on the platform. **Discount %:** (MRP - selling price) / MRP.
- **Bank offer:** an extra reduction for paying with certain cards, often funded by the bank or the platform. It lowers the effective price only for eligible buyers.
- **Why an average discount misleads:** a simple average gives every product equal weight. Take two products (invented): ₹1,000 MRP sold at ₹800 (20% off) and ₹10,000 MRP sold at ₹9,000 (10% off). The simple average is 15%, but the true overall discount is 1 - 9,800/11,000 = **10.9%**, about 11%. Weight by MRP or sales value.
- Also compare like with like: the MRP itself may be inflated, so a deep discount does not always mean a cheap price.
**Worked example:** headline = (20,000 - 15,000) / 20,000 = **25%**. Effective price = 15,000 - 1,000 = ₹14,000; effective discount = 6,000 / 20,000 = **30%**, which is 5 percentage points above the headline.
**Likely follow-ups:** 1) *Who pays for the bank offer?* Depends on the deal; check the funding split. 2) *Which discount is net revenue based on?* It depends on how finance books bank offers (reduction of price or a marketing cost); ask finance.
**Common mistakes:** Subtracting percentages instead of working in rupees; simple-averaging discounts across items of different value.

### Q40 ⭐⭐ 🟡 How would you test whether a discount coupon created extra orders rather than just discounting orders that would have happened anyway?
Data: 10,000 customers got a ₹75 coupon and placed 25,000 orders, all using the coupon. A similar control group of 10,000 customers got no coupon and placed 20,000 orders. Calculate incremental orders and coupon cost per incremental order.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you use a control group to measure incrementality, not raw coupon orders.
**Say this in the interview:** "Compare the coupon group to a control group. The extra orders are 25,000 minus 20,000 = 5,000. The coupon cost ₹18,75,000, so each incremental order cost ₹375, far above the ₹75 face value."
**Explain simply:**
- **Incremental orders:** orders that happened only because of the coupon. The control group shows what would have happened anyway.
- The control must be similar and chosen randomly; otherwise keen buyers in one group distort the answer.
- Here 20,000 of the 25,000 coupon orders (80%) would probably have happened anyway, yet all got the discount.
- Decide with economics: if an average order earns ₹100 contribution (invented), paying ₹375 per extra order loses money unless the customer later keeps buying. Check repeat behaviour after the coupon ends.
**Worked example:** orders per customer: 2.5 (coupon) vs 2.0 (control), a lift of 0.5 per customer. Incremental orders = 25,000 - 20,000 = **5,000**. Coupon cost = 25,000 x ₹75 = ₹18,75,000. Cost per incremental order = 18,75,000 / 5,000 = **₹375**.
**Likely follow-ups:** 1) *Is the difference real?* Check it is bigger than random noise: a statistical test, or a range (confidence interval) around the 5,000 that does not include zero. 2) *What else to watch?* Pull-forward, where customers just bring future orders earlier.
**Common mistakes:** Dividing cost by all coupon orders (₹75) instead of incremental ones; comparing with last month instead of a concurrent control.

### Q41 ⭐⭐ 🟡 Who funds a discount on a marketplace (seller, brand or platform), and why does it matter for net revenue and margin?
Data: MRP ₹1,000; selling price ₹800. The seller funds ₹100 of the discount and the platform funds ₹100.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you separate what the customer pays from who bears the cost.
**Say this in the interview:** "The customer pays ₹800, a ₹200 discount. The seller bears ₹100 and the platform bears ₹100. The platform's ₹100 is a cost to it, so its margin is lower than the headline GMV suggests."
**Explain simply:**
- A discount can be funded by the seller, the brand (for example a promotion funded by the manufacturer), or the platform from its own budget.
- Using the figures given: customer pays 800. The seller effectively receives 1,000 - 100 (its own share) = 900 before fees, because the platform tops up its 100 share (assumed here; terms vary by contract).
- Platform: collects 800 from the customer, passes 900 to the seller, so it is out of pocket 100, before commissions it earns.
- How this is booked in accounts (reduction of revenue or a marketing expense) varies; ask finance.
- Matters because: seller margin, platform margin and the "true" discount rate differ; and a platform-funded discount is a marketing cost that must pay for itself.
**Worked example:** total discount = 1,000 - 800 = 200 = 20% of MRP. Seller share 100 (50%), platform share 100 (50%). Platform subsidy per order = ₹100, which is 12.5% of the selling price of 800.
**Likely follow-ups:** 1) *Which table shows it?* A promotions or order-item discount table with funding-source columns. 2) *Why does a seller care?* Their payout falls by their share.
**Common mistakes:** Treating the whole discount as lost revenue to the platform; ignoring who funded it when computing seller margin.

### Q42 ⭐⭐ 🟡 What is a contact rate in customer support, and which reason tags (for example "where is my order") would you analyse first?
Data: 2,50,000 orders and 15,000 support tickets in a week; 6,000 tickets were "where is my order". Calculate the contact rate per 100 orders and the share of such tickets.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can normalise support volume by orders and prioritise reasons.
**Say this in the interview:** "The contact rate is 6 tickets per 100 orders. 'Where is my order' is 40% of tickets, or 2.4 per 100 orders, so I would start there."
**Explain simply:**
- **Contact rate:** support tickets (or calls and chats) per 100 orders; it tells you how often a delivery triggers a complaint.
- **Reason tag:** the category an agent picks for a ticket. Common tags: where is my order, late delivery, missing or wrong item, damaged item, refund status, payment problem.
- Start with the biggest tag by volume, then the ones with the highest cost per ticket or worst customer satisfaction.
- "Where is my order" often signals that delivery status updates or ETA are weak; improving tracking messages can cut it.
- Check tag quality: agents may pick the first tag in a list, so a large "other" bucket is a warning.
**Worked example:** contact rate = 15,000 / 2,50,000 x 100 = **6.0 per 100 orders**. WISMO share = 6,000 / 15,000 = **40%**. WISMO per 100 orders = 6,000 / 2,50,000 x 100 = **2.4**.
**Likely follow-ups:** 1) *Should tickets match the same week's orders?* Ideally track by order cohort, since tickets lag orders. 2) *What cuts?* City, courier, delay bucket, new vs repeat customers.
**Common mistakes:** Quoting raw ticket counts without orders as the denominator; trusting tags without sampling tickets.

### Q43 ⭐⭐ 🟡 What are first-attempt delivery rate and an NDR (non-delivery report), and how do they drive RTO?
Data: 20,000 shipments; 17,000 delivered on the first attempt; 2,500 raised an NDR, of which 1,000 were delivered on re-attempt; the rest returned to origin. Calculate the first-attempt rate and the RTO count.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can follow a failed delivery through the NDR step to RTO and spot unaccounted shipments.
**Say this in the interview:** "First-attempt rate is 85%. Of 2,500 NDRs, 1,500 ended as RTO, so RTO is 7.5% of shipments. Note that 500 shipments are unaccounted for in the data."
**Explain simply:**
- **First-attempt delivery rate:** shipments delivered on the first try / total shipments.
- **NDR (non-delivery report):** the courier's report that delivery failed, with a reason such as customer not available, wrong address or customer refused.
- **RTO (return to origin):** the parcel goes back to the seller. Each NDR is a chance to save the order by calling the customer or fixing the address; failed saves become RTOs.
- The data does not add up: 17,000 + 2,500 = 19,500, leaving 500 shipments (2.5%) unexplained. They may be in transit, cancelled or lost. I would ask rather than assume.
**Worked example:** first-attempt rate = 17,000 / 20,000 = **85.0%**. NDR rate = 2,500 / 20,000 = 12.5%. RTO count = 2,500 - 1,000 = **1,500**, which is 7.5% of shipments and 60% of NDRs. NDR recovery rate = 1,000 / 2,500 = 40%. Total delivered = 18,000 = 90%.
**Likely follow-ups:** 1) *Which lever cuts RTO most?* Better NDR resolution within 24 hours. 2) *Which cuts?* NDR reason, courier, pincode, COD vs prepaid.
**Common mistakes:** Calling every NDR an RTO; ignoring shipments still in transit; dividing RTO by delivered rather than dispatched shipments.

### Q44 ⭐⭐ 🟡 How do you measure delivery-partner productivity and cost, and which numbers would you show a city operations head?
Data (one rider-day): 8 hours logged in, 2 hours idle, 20 orders delivered, ₹1,200 total pay and incentives. Calculate orders per logged-in hour, orders per active hour and cost per order.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate logged-in time from active time and link productivity to cost.
**Say this in the interview:** "That rider did 2.5 orders per logged-in hour, 3.33 per active hour, at ₹60 per order. I would show the city head these three plus idle share and incentive share of pay."
**Explain simply:**
- **Logged-in hours:** time the rider was available on the app. **Active hours:** logged-in minus idle (waiting with no order).
- Orders per logged-in hour shows how well supply is used; orders per active hour shows the rider's effort. A big gap means too many riders for the demand at that time.
- **Cost per order:** total pay and incentives / orders delivered. Incentives (extra pay for peak hours or order targets) can push this up.
- Show the head: orders per hour by hour of day, idle share, cost per order by zone, share of riders under a minimum earning level, and attendance. These are averages across many riders, so show the spread too.
**Worked example:** logged-in 8 h, idle 2 h, active 8 - 2 = 6 h. Orders per logged-in hour = 20 / 8 = **2.5**. Orders per active hour = 20 / 6 = **3.33**. Cost per order = 1,200 / 20 = **₹60**. Idle share = 2 / 8 = 25%.
**Likely follow-ups:** 1) *Why not just maximise orders per hour?* Rushed riders risk safety and quality. 2) *Why cost per order rises on rainy days?* Incentives and longer trips.
**Common mistakes:** Using total hours as the only denominator; ignoring one-day noise in a single rider-day.

### Q45 ⭐⭐ 🟡 Which workforce metrics (attendance, shift fill, productivity per picker hour, attrition) would you track for dark store pickers and delivery partners, using your HR background?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question, not drawn from a specific company report.
**What the interviewer is checking:** Whether you can bring HR measurement skills to an operations workforce.
**Say this in the interview:** "I would track attendance, shift fill, productivity per hour and attrition, and tie each to service levels such as pick time and late orders. My HR background helps me define attrition and attendance consistently."
**Explain simply:**
- **Attendance:** days present / days rostered. **Shift fill rate:** shifts filled / shifts planned; low fill at peak hours directly hurts delivery times.
- **Productivity per picker hour:** orders (or items) picked / paid picker hours; compare by shift and store.
- **Attrition:** people who left in a period / average headcount. For gig partners, define "left" clearly, for example no order in 30 days.
- **Early attrition:** share leaving within 30 or 60 days; it points to onboarding or pay problems.
- **Earnings per hour** and **overtime or incentive share:** link to retention.
- Join with operations data: late share, pick time and fill rate by shift. Handle individual-level data carefully; report at store or team level.
**Likely follow-ups:** 1) *Employee vs gig partner?* Different legal status and data, so keep definitions separate. 2) *First chart?* Shift fill by hour against orders.
**Common mistakes:** Using a different attrition definition for riders and pickers without saying so; ignoring seasonality; reporting only averages.

### Q46 ⭐⭐ 🟡 Your platform onboards delivery partners. How would you analyse the onboarding funnel and where would you look for drop-off?
Data (one month): 10,000 applied; 6,000 documents verified; 4,500 trained; 3,600 took a first order; 2,000 still active after 30 days. Calculate step-wise and overall conversion.
**Asked at:** commonly asked (no company-specific report found); a gap-fill question.
**What the interviewer is checking:** That you compute step-wise conversion and use it to find where to act.
**Say this in the interview:** "Conversion is 60%, 75%, 80% and 55.6% step by step, and 20% overall. The biggest loss in count is at document verification, and the biggest relative loss after the first order, so I would look at both."
**Explain simply:**
- **Funnel:** an ordered list of steps; step conversion is each step divided by the previous one.
- Losses: 4,000 lost at verification, 1,500 at training, 900 before the first order, 1,600 after the first order.
- Split each step by city, source of application, vehicle type and week of applying. Look at time between steps, since long waits cause drop-off.
- Late drop-off (after the first order) points to earnings, order availability or support rather than paperwork.
- One caution: a month's data mixes people who applied late in the month and have not yet had time to progress. A cohort view (track each week's applicants) is cleaner.
**Worked example:** applied to verified 6,000 / 10,000 = **60.0%**; verified to trained 4,500 / 6,000 = **75.0%**; trained to first order 3,600 / 4,500 = **80.0%**; first order to active at 30 days 2,000 / 3,600 = **55.6%**; overall 2,000 / 10,000 = **20.0%**.
**Likely follow-ups:** 1) *Where do you act first?* The largest count loss that is fixable, such as document rejections. 2) *Is 20% good?* Compare with your own past months, not outside benchmarks.
**Common mistakes:** Multiplying percentages wrongly; ignoring the cohort timing problem; treating every drop-off as the partner's fault.

### Q47 ⭐⭐ 🟡 How would you tell the difference between wastage (known losses) and shrinkage (unexplained loss) for a fresh category in a dark store?
Data: 5,000 kg of produce received; 4,500 kg sold; 300 kg recorded as expired or damaged; the rest unaccounted for. Calculate the wastage, shrinkage and total loss percentages.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you separate recorded from unexplained loss and question the stock balance.
**Say this in the interview:** "Wastage is the recorded 300 kg, 6% of what was received. The remaining 200 kg is unexplained shrinkage, 4%, so total loss is 10%. I would treat shrinkage as the one to investigate."
**Explain simply:**
- **Wastage:** loss that is recorded with a reason, such as expiry or damage.
- **Shrinkage:** loss that stock records cannot explain, such as theft, counting or weighing error, missing receipts or unrecorded damage.
- Premise: the data ignores opening and closing stock; I assume none was left at the start or end. In practice, include them, and note that fresh produce also loses weight through drying, which can look like shrinkage.
- To investigate shrinkage: compare cycle-count (periodic physical count) results with system stock, check by shift, by receiving batch, and by SKU.
**Worked example:** received 5,000 kg; sold 4,500; recorded wastage 300; unaccounted = 5,000 - 4,500 - 300 = 200 kg. Wastage = 300 / 5,000 = **6.0%**. Shrinkage = 200 / 5,000 = **4.0%**. Total loss = 500 / 5,000 = **10.0%**. Percentages are of quantity received, in weight, not value.
**Likely follow-ups:** 1) *Weight or value?* Report both; value reflects price. 2) *How to cut wastage?* Better demand forecasts and smaller orders.
**Common mistakes:** Using sales as the denominator; mixing weight and value; ignoring opening and closing stock.

### Q48 ⭐⭐ 🟡 How do items per order and AOV together explain a change in basket size, and what would you check?
Data: week 1 had 10,000 orders and 32,000 items; week 2 had 11,000 orders and 40,700 items. Calculate items per order for each week and say what could explain the change.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can split basket growth into items and price and avoid a single explanation.
**Say this in the interview:** "Items per order went from 3.2 to 3.7, up about 15.6%, while orders rose 10%. Total items rose about 27.2%. To explain AOV I need the order value: AOV equals items per order times average price per item."
**Explain simply:**
- **Items per order (IPO):** items / orders. **AOV (average order value):** order value / orders. AOV = IPO x average item price.
- So AOV can rise because baskets hold more items, or because items cost more, or both. Week-wise GMV is not given, so I cannot compute AOV; I would ask for it.
- Possible reasons for the rise: a minimum-order or free-delivery threshold, a basket-building promotion, a mix shift to cheaper small items, a new category, a festival week, or more repeat customers.
- Checks: item count by category, price per item, share of orders above the free-delivery threshold, and new vs repeat customers.
**Worked example:** week 1 IPO = 32,000 / 10,000 = **3.2**; week 2 IPO = 40,700 / 11,000 = **3.7**. Change in IPO = +0.5 items, +15.6%. Orders +10.0%; total items +27.2%.
**Likely follow-ups:** 1) *What if IPO rises but AOV falls?* Cheaper items; check mix. 2) *Is one week enough?* No; compare with more weeks and the same weekday pattern.
**Common mistakes:** Assuming more items means higher AOV; treating a one-week change as a trend.

### Q49 ⭐⭐ 🟡 What is the minimum AOV at which a quick-commerce order breaks even on contribution, given the cost lines below?
Data per order: gross margin 18% of AOV; ads income ₹10; pick-and-pack ₹25; last-mile delivery ₹45; payment and other costs ₹10; allocated store cost ₹15.
**Asked at:** commonly asked (no company-specific report found); unit-economics and break-even questions are common in quick-commerce case rounds (unverified, prep-site level).
**What the interviewer is checking:** Whether you can turn cost lines into one equation and solve it, and whether you know what "contribution" means.
**Say this in the interview:** "Break-even AOV is where margin plus ads income equals all per-order costs. Here that is about ₹473 per order; below it we lose money on each order."
**Explain simply:**
- **AOV** (average order value) is the rupee value of one basket. **Gross margin** is the share of that basket we keep after paying suppliers, so it grows with AOV.
- **Contribution** is what one order earns after the costs that exist because of that order. Costs here are fixed in rupees per order, so only margin moves with basket size.
- Some firms leave out allocated store cost (rent shared across orders) and call the rest "contribution". Definitions differ; I state mine and include it.
**Worked example:**
- Costs per order: 25 + 45 + 10 + 15 = ₹95. Ads income: ₹10, so margin must cover 95 - 10 = ₹85.
- 0.18 x AOV = 85, so AOV = 85 / 0.18 = ₹472.22, rounded up to ₹473 (at ₹473, contribution is about +₹0.14).
- Check: at ₹400 contribution is -₹13; at ₹500 it is +₹5; at ₹600 it is +₹23. Each extra ₹100 of basket adds ₹18.
- Without the ₹15 store cost, break-even is 70 / 0.18 = ₹388.89.
**Likely follow-ups:** 1) *How do you lift contribution?* Raise AOV (bundles, free-delivery thresholds), raise ads income, cut delivery cost through batching. 2) *Is margin really 18% for every basket?* No; it is an average, and mix shifts change it.
**Common mistakes:** Forgetting ads income; treating costs as a percentage of AOV when they are fixed per order; quoting break-even without saying which costs are included.

### Q50 ⭐⭐ 🟡 How do you connect app or web session events (clickstream) to orders, and what attribution problems arise?
**Asked at:** commonly asked (no company-specific report found); funnel and clickstream joins appear in e-commerce analyst guides (unverified).
**What the interviewer is checking:** That you know the join keys and can name why the join is never perfect.
**Say this in the interview:** "I join on a shared ID, usually user or session ID plus time, so each order points to the session that led to it. Then I note the gaps: logged-out browsing, several devices and several touchpoints."
**Explain simply:**
- **Clickstream** is the log of every tap or page view (open app, search, add to cart). **Attribution** means deciding which session or campaign gets credit for an order.
- Best case: the order event carries the session ID. Otherwise join on user ID and take the last session that started before the order.
- Problems: guests with no user ID; one person on phone and laptop (two IDs); cookie or app-reinstall resets; clocks that differ between app and server; one order after several visits (last click, first click or split credit give different answers); orders placed by call or from a push notification.
**Data and tables involved:** `sessions` (session_id, user_id, device_id, start time, source/campaign), `events` (session_id, event name, time), `orders` (order_id, user_id, ordered_at).
```sql
-- credit each order to the latest session that started before it
select o.order_id, o.user_id,
  (select s.session_id from sessions s
   where s.user_id = o.user_id and s.started_at <= o.ordered_at
   order by s.started_at desc limit 1) as session_id
from orders o;
```
Output (small sample): order 11 maps to session s2, order 12 to s3, order 13 to s1. Plain words: each order is tied to the user's most recent earlier visit; add a time limit (for example 24 hours) in real work.
**Likely follow-ups:** 1) *Last click or first click?* Say which you use; last click favours the final nudge, first click favours discovery. 2) *How do you spot a broken join?* Share of orders with no session should be small and stable.
**Common mistakes:** Joining on user ID alone with no time rule; assuming 100% match; not telling the business which attribution rule you used.

### Q51 ⭐⭐ 🟡 How is a session defined on an app or website, and why can session counts differ between a web-analytics tool and your own event data?
**Asked at:** commonly asked (no company-specific report found); session definitions are a standard product-analytics topic (unverified).
**What the interviewer is checking:** That you know "session" is a rule someone chose, not a natural fact.
**Say this in the interview:** "A session is a group of one user's events with no long pause between them. Tools and our own SQL use different pause limits and reset rules, so counts rarely match."
**Explain simply:**
- Common rule (from memory, unverified; varies by tool): a session ends after about 30 minutes of inactivity. A new session also starts at midnight in some tools, or when the traffic source changes in others.
- Differences arise from: different timeout; app backgrounding counted differently; bot traffic filtered by the tool but not in raw data; consent banners (users who decline are missing from the tool but present in server logs); ad blockers; different time zones; sampling in some tools.
- So compare trends, not absolute counts, and write your definition next to every number.
- HR analogy: "active employee" can mean on payroll, or badge-swiped this week; same word, different counts.
**Likely follow-ups:** 1) *Which count is right?* Neither; pick one as the source of truth for the business and document it. 2) *How do you reconcile?* Rebuild the tool's rules in SQL on a sample day and compare.
**Common mistakes:** Mixing session counts from two systems in one chart; ignoring time zone; treating a session as a person.

### Q52 ⭐⭐ 🟡 What does a catalogue analyst check (duplicate listings, missing attributes, wrong categories, poor images), and how does bad catalogue data affect conversion and returns?
**Asked at:** commonly asked (no company-specific report found); catalogue integrity appears in e-commerce catalogue-analyst job postings (Myntra, Randstad; unverified, snippet level).
**What the interviewer is checking:** That you see the catalogue as data that can be audited and tied to money.
**Say this in the interview:** "I audit four things: the same product listed twice, blank or wrong attributes, wrong category, and weak images. Then I compare conversion and return rates of clean and unclean listings."
**Explain simply:**
- The **catalogue** is the master list of products shown to customers. A **SKU** is one sellable variant (for example, a blue shirt in size M).
- **Duplicates:** same product under different titles splits reviews and sales; find via same barcode/brand/size, or near-identical titles.
- **Missing attributes:** size, colour, weight, material blank means filters fail and the product is not found.
- **Wrong category:** appears in wrong search results, wrong commission or tax rate applied.
- **Poor images:** low count or low resolution lowers trust.
- Effects: lower conversion (customers cannot find or trust it) and higher returns (item differs from expectation, "not as described").
**Data and tables involved:** `catalogue` (sku, title, brand, category, attributes, image count), `sessions/product views`, `orders`, `returns` (with reason). First cut: completeness percentage per attribute per category; conversion and return rate for listings with and without full attributes.
**Likely follow-ups:** 1) *How do you prioritise fixes?* By views and sales at stake, not by count of errors. 2) *Cause or correlation?* Poor listings may simply be low-quality products; compare within a category.
**Common mistakes:** Counting errors without business impact; fixing rare SKUs first; ignoring return reasons.

### Q53 ⭐⭐ 🟡 Which fraud and abuse patterns appear in e-commerce (coupon abuse, return fraud, fake COD orders, refund abuse), and what data would flag them?
**Asked at:** commonly asked (no company-specific report found); COD returns-to-origin (RTO) losses are widely discussed in press (figures unverified, not used here).
**What the interviewer is checking:** That you think in patterns and signals, and stay fair to genuine customers.
**Say this in the interview:** "Each abuse leaves a pattern in the data: many accounts on one device or address, unusual return or refund rates per customer, and COD orders refused at the door. I flag by rules first and review before blocking."
**Explain simply:**
- **Coupon abuse:** one person creates many accounts to reuse a new-user offer. Signals: same phone, device, address or payment instrument across accounts.
- **Return fraud:** wrong item sent back, used item, empty box. Signals: return rate far above peers, returns concentrated in high-value items, repeat "item not received".
- **Fake COD orders:** cash-on-delivery orders placed with no intent to accept. Signals: new account, new pincode, high value, past refusals; the order comes back as RTO (return to origin).
- **Refund abuse:** claiming "damaged" or "missing" repeatedly. Signals: refund claims per customer, per rider, per store.
- Always measure the false-positive cost: a false positive is a genuine customer wrongly flagged, and blocking them loses real revenue.
**Data and tables involved:** `orders`, `customers` (phone, device, address hash), `coupons`, `returns/refunds`, `delivery outcomes`. First cut: customers per device/address, refund share by customer decile.
**Regulation / privacy note (awareness only):** Matching devices and phones is personal-data processing; from memory, unverified, confirm with the compliance/legal team.
**Likely follow-ups:** 1) *Rules or model?* Start with simple rules; a model needs reliable fraud labels. 2) *How do you size the loss?* Fraud value over total value, by type.
**Common mistakes:** Labelling heavy but honest buyers as fraud; one rule for all categories; no feedback loop on blocked orders.

### Q54 ⭐⭐ 🟡 Which date do you use to report an order to a month: order date, payment date, dispatch date or delivery date, and how does the choice change the numbers?
Data: an order for ₹1,000 was placed on 30 November, delivered on 3 December and returned on 10 December. Show how each date convention reports it.
**Asked at:** commonly asked (no company-specific report found); "which date" is a classic MIS and reporting-definition question (unverified).
**What the interviewer is checking:** That you know one order has many dates and that the choice must match the purpose.
**Say this in the interview:** "It depends on the question. Order date for demand, delivery date for revenue recognised, and I always report returns against the month they happen or against the original order, but never mix the two silently."
**Explain simply:**
- **Order date:** when the customer placed it; shows demand (GMV, gross merchandise value).
- **Payment date:** when money arrived; useful for cash. For COD it is the delivery date.
- **Dispatch date:** when it left the warehouse; used for warehouse workload.
- **Delivery date:** when the customer got it; the usual basis for revenue or net sales (finance rules differ; confirm with finance).
- A return can be shown by its own date (December) or pushed back to the original order month (November).
**Worked example:** (the question gives no payment or dispatch date; I assume payment on 30 Nov for a prepaid order, and dispatch on 1 Dec.)

| Convention | Month the Rs 1,000 lands in | Return of Rs 1,000 |
|---|---|---|
| Order date | November | December if by return date; November if matched back to order |
| Payment date (prepaid) | November | December |
| Dispatch date (assumed 1 Dec) | December | December |
| Delivery date | December | December |

Under return-date reporting, November shows +1,000 on an order-date basis and December shows -1,000 with no sales; delivery-date basis nets December to zero. Same order, three different monthly stories.
**Likely follow-ups:** 1) *Which do finance use?* Usually delivery-based; ask. 2) *How do you stop disputes?* Publish the definition on the dashboard.
**Common mistakes:** Comparing a dashboard on order date to finance on delivery date; leaving return months unmatched; ignoring orders crossing month end.

### Q55 ⭐⭐ 🟡 Which customer data in an orders table is personal information (name, phone, address, location), and how would you share data safely with a business team?
**Asked at:** commonly asked (no company-specific report found); data-handling questions are common for analyst roles (unverified).
**What the interviewer is checking:** That you notice personal data without being told, and share the minimum needed.
**Say this in the interview:** "Name, phone, email, full address and precise location are personal data, and so are IDs that can be traced back to a person. I share only the columns the team needs, in masked or grouped form."
**Explain simply:**
- Direct identifiers: name, phone, email, delivery address, precise latitude and longitude, device ID, payment details.
- Indirect: customer ID, pincode plus order time (a rare combination can identify someone).
- Safe sharing: drop columns not needed; replace customer ID with a masked key; use pincode or area instead of address; aggregate (counts and averages by area) instead of row-level data; restrict access and log who has the file; do not email raw extracts or paste into personal tools.
- HR parallel: you would never send the whole employee master with salaries to a department head.
**Regulation / privacy note (awareness only):** Principle is purpose limitation and data minimisation. Details of Indian law: from memory, unverified, confirm with the compliance/legal team.
**Likely follow-ups:** 1) *Is hashing enough?* Not always; hashed phone numbers can be re-derived by guessing, so use a salted key. 2) *Small groups?* Hide cells with very few customers.
**Common mistakes:** Sharing the full orders table "just in case"; thinking removing the name is enough; screenshots with phone numbers.

### Q56 ⭐⭐ 🟡 In plain words, what should an e-commerce analyst know about India's Digital Personal Data Protection Act, 2023, when using customer data for analysis?
**Asked at:** commonly asked (no company-specific report found); awareness-level question; source explainers disagree on details such as analytics (unverified).
**What the interviewer is checking:** That you know the basic principles and know when to ask legal instead of guessing.
**Say this in the interview:** "I am not a lawyer, but I know the ideas: use personal data only for the purpose the customer agreed to, collect only what is needed, keep it only as long as needed, and keep it secure. For anything unclear I check with the compliance team."
**Explain simply:** All points from memory, unverified, confirm with the compliance/legal team.
- Customers should give clear **consent** for stated purposes; using data for a new purpose may need fresh consent or another lawful ground.
- **Data minimisation:** analysts should request only needed columns.
- **Retention:** data should not be kept forever once the purpose ends; customers may ask for correction or erasure.
- **Security and breach:** a leak of an extract is a serious incident that must be reported internally at once.
- Analyst habits: use masked or aggregated data, no downloads to personal devices, document where each dataset came from and why you need it.
**Regulation / privacy note (awareness only):** This is not legal advice. Dates, penalties and exemptions: unverified; ask legal.
**Likely follow-ups:** 1) *Can I analyse purchase history for recommendations?* Depends on consent wording; ask legal. 2) *What if a customer asks for deletion?* Follow the company process; tell the data owner.
**Common mistakes:** Quoting penalty amounts or section numbers confidently; saying "it doesn't apply to analytics"; keeping local copies.

### Q57 ⭐⭐ 🟡 What is order processing time or dispatch SLA in an e-commerce warehouse, and how would you measure breaches?
Data: 5,000 orders were due to be dispatched within 24 hours of payment; 4,350 were dispatched in time. Calculate the dispatch-SLA compliance and the breach count, and list cuts you would run on the breaches.
**Asked at:** commonly asked (no company-specific report found); pick time and dispatch time appear in fulfilment-metric explainers (vendor blogs, unverified).
**What the interviewer is checking:** That you can define the clock (start and stop) and compute a clean compliance rate.
**Say this in the interview:** "Compliance is on-time orders over orders due: 4,350 of 5,000 is 87%, so 650 breaches, 13%. Then I cut the breaches by warehouse, hour, category and reason."
**Explain simply:**
- **Order processing time** is the time from payment (clock start) to dispatch from the warehouse (clock stop). **SLA** (service level agreement) is the promised limit, here 24 hours.
- Orders still not dispatched past 24 hours also count as breaches; do not leave them out because they have no stop time.
- Denominator is orders whose deadline has passed, not all orders placed today.
**Worked example:** 4,350 / 5,000 = 87.0%. Breaches: 5,000 - 4,350 = 650, which is 13.0% of orders.
**Data and tables involved:** `orders` (paid_at, dispatched_at, warehouse, category, seller). Cuts: warehouse, hour of payment, day of week, category, seller, stock-out reason, carrier pickup time.
```sql
select warehouse, count(*) as orders_due,
  sum(case when dispatched_at is not null
        and (julianday(dispatched_at) - julianday(paid_at)) * 24 <= 24
      then 1 else 0 end) as on_time,
  sum(case when dispatched_at is null
        or (julianday(dispatched_at) - julianday(paid_at)) * 24 > 24
      then 1 else 0 end) as breaches
from orders group by warehouse;
```
On five sample orders the output was North: 2 due, 1 on time, 1 breach; South: 3 due, 1 on time, 2 breaches. Plain words: the null (never dispatched) order counts as a breach.
**Likely follow-ups:** 1) *Business hours or calendar hours?* State it; Sunday orders look bad on calendar hours. 2) *Is 87% good?* Compare with target and trend.
**Common mistakes:** Dropping undispatched orders; using order date instead of payment time; averaging hours instead of reporting the share within SLA.

### Q58 ⭐⭐ 🟡 What is ETA accuracy in quick commerce, and how would you measure the gap between the delivery time shown to the customer and the actual time?
Data: 10 orders showed an ETA of 12 minutes; the actual times were 9, 10, 11, 12, 12, 13, 14, 15, 18 and 22 minutes. Calculate the average error, the share on time or early, and the 90th-percentile time.
**Asked at:** commonly asked (no company-specific report found); delivery-time terms are core quick-commerce vocabulary (unverified).
**What the interviewer is checking:** That you see an average can hide the late tail, and that you use several measures.
**Say this in the interview:** "ETA accuracy is how close the promised time is to the real time. Here the average error is +1.6 minutes late, 50% were on time or early, and the 90th percentile is 18.4 minutes, so the tail is the problem."
**Explain simply:**
- **ETA** (estimated time of arrival) is the time promised on the app. **Error** = actual minus ETA; positive means late.
- Report signed error (bias), absolute error (size of miss), on-time share, and a high percentile.
- A **percentile** answers "nine in ten orders arrive within X minutes".
**Worked example:**
- Errors: -3, -2, -1, 0, 0, +1, +2, +3, +6, +10. Average signed error = +1.6 minutes (late on average).
- Average absolute error = 2.8 minutes.
- On time or early (actual <= 12): 9, 10, 11, 12, 12 = 5 of 10 = 50%.
- 90th percentile: 18.4 minutes (linear interpolation, as Excel PERCENTILE.INC); nearest-rank method gives 18. State the method.
- Average actual time is 13.6 minutes; median 12.5.
**Likely follow-ups:** 1) *Grace window?* Many teams count within one or two minutes as on time; define it. 2) *Why show early arrivals separately?* Over-padded ETAs are safe but hurt conversion.
**Common mistakes:** Netting early against late so errors cancel; using only the mean; not saying which percentile method.

### Q59 ⭐⭐ 🟡 Why can a customer order an item shown as in stock and then have it cancelled, and which data would show inventory accuracy problems?
**Asked at:** commonly asked (no company-specific report found); fill rate and availability appear in quick-commerce explainers (vendor blogs, unverified).
**What the interviewer is checking:** That you understand the gap between system stock and physical stock.
**Say this in the interview:** "The app shows system stock, not what is on the shelf. When they differ, the picker cannot find the item and the order line is cancelled. I measure that gap with counts, picking failures and cancellations by reason."
**Explain simply:**
- Causes: damaged or expired items not written off in the system; theft or miscounts; items put in the wrong bin; two customers buying the last unit at nearly the same time; late stock updates from sellers; a delay between a physical event and its system entry.
- A **dark store** is a small warehouse used only for fast delivery, so even small errors hit many orders.
- **Fill rate** is the share of ordered units actually supplied.
**Data and tables involved:** `inventory` (sku, store, system qty), `cycle count` (physical qty on a count date), `pick events` (item not found), `cancellations` (reason = out of stock), `adjustments` (write-offs). First cuts: inventory record accuracy (SKUs where system equals physical, over SKUs counted), item-not-found rate by store and category, cancellations per 1,000 orders.
**Likely follow-ups:** 1) *Fix?* More frequent counts on fast movers, buffer stock limits on the app. 2) *Business impact?* Lost sales and lost trust.
**Common mistakes:** Blaming demand forecasts only; ignoring write-off timing; counting cancellations with no reason code.

### Q60 ⭐⭐ 🟡 How would you analyse refund turnaround time, and how do orders, payment-gateway and bank records get reconciled for refunds?
**Asked at:** commonly asked (no company-specific report found); payment and settlement vocabulary comes from payments-vendor explainers (unverified).
**What the interviewer is checking:** That you can track a refund across three systems and spot where it gets stuck.
**Say this in the interview:** "Refund turnaround is the time from refund request or approval to money credited. I measure it by stage and then reconcile refund records between our orders system, the payment gateway and the bank."
**Explain simply:**
- A **payment gateway** is the service that moves card or UPI payments between customer and business. **Reconciliation** means matching records between systems and explaining differences.
- Stages: refund requested, approved, initiated at gateway, processed by bank, credited to customer. Measure median and 90th percentile days for each stage.
- Reconcile on refund ID or order ID and amount: refunds in orders but not at gateway (stuck), at gateway but not at bank (in transit), amount mismatches (partial refunds, fees).
- Cut by payment method (UPI, card, wallet, COD refund to store credit), reason, and days pending.
**Data and tables involved:** `refunds` (order_id, requested_at, approved_at, amount), `gateway_refunds` (refund_ref, initiated_at, status), `bank_credits` (reference, credited_at, amount).
**Likely follow-ups:** 1) *Which metric for the dashboard?* Percent refunded within promised days, plus an ageing list of open refunds. 2) *Unmatched ones?* Escalate by age bucket.
**Common mistakes:** Using average only; starting the clock at order date; ignoring pending refunds.

### Q61 ⭐⭐ 🟡 How would you use hourly order data to plan pickers and riders, and how do you define a peak hour?
**Asked at:** commonly asked (no company-specific report found); orders per store per day is common quick-commerce vocabulary (unverified).
**What the interviewer is checking:** That you can turn demand into staffing, using a clear peak definition.
**Say this in the interview:** "I build an hourly demand profile by day type and store, then divide by what one picker or rider can handle per hour. A peak hour is an hour whose orders exceed a stated threshold, for example the top 10% of hours or 1.5 times the daily average."
**Explain simply:**
- A **picker** collects items in the dark store; a **rider** delivers. Each has a capacity (orders per hour) that you measure from past data.
- Required staff for an hour = expected orders / capacity per person, plus a buffer for rain, offers and no-shows.
- Use at least several weeks of data; split weekday, weekend and festival days; forecast per store, not for the city.
- HR link: this is shift planning with attendance risk; compare scheduled against logged-in staff.
**Data and tables involved:** `orders` (store, placed_at), `shift roster`, `rider logins`, `pick time`. First cut: orders by hour and weekday heatmap, orders per active picker per hour.
**Likely follow-ups:** 1) *Why not use daily totals?* The shortage occurs in a few hours. 2) *How do you test the plan?* Compare delivery time and cancellations in peak hours before and after.
**Common mistakes:** Using the city average for every store; ignoring day type; defining peak by feel.

### Q62 ⭐⭐ 🟡 How would you measure the time between a customer's orders in quick commerce, and what does a long gap tell you?
Data: a new customer cohort of 1,000 users; 600 placed a second order within 30 days; 300 placed a third within 60 days. Calculate the 30-day repeat rate and the second-to-third order conversion.
**Asked at:** commonly asked (no company-specific report found); repeat and churn analysis appears in reported Flipkart rounds (anonymous reviews, unverified).
**What the interviewer is checking:** That you handle cohort definitions and window rules properly.
**Say this in the interview:** "I use a window function (a SQL feature that can look at the previous row) to get the gap between each order and the previous one. Here the 30-day repeat rate is 60%, and 50% of second-time buyers go on to a third order."
**Explain simply:**
- **Cohort:** customers who joined (first order) in the same period. Gap = this order date minus previous order date, per customer.
- Long gap means weaker habit or churn risk; look at the median gap and the share beyond 30 days.
- Only judge customers who have had the full window to repeat.
**Worked example:**
- 30-day repeat rate = 600 / 1,000 = 60.0%.
- Second-to-third conversion = 300 / 600 = 50.0% (the data says third order within 60 days; I assume this is the same 600, so the bases are consistent).
- Third order as a share of the cohort: 300 / 1,000 = 30.0%.
```sql
select user_id, order_date,
  julianday(order_date) - julianday(lag(order_date) over (partition by user_id order by order_date)) as days_since_previous
from orders;
```
Output on a 3-row sample: user u1 has orders on 1 and 10 November, so the second row shows 9 days since the previous order; each first order shows empty (null). In plain words: `lag` looks at the user's previous row, so the date difference is the gap; the first order has no gap.
**Likely follow-ups:** 1) *Which gap is "long"?* Compare with the category's normal buying cycle. 2) *Mean or median?* Median; a few very long gaps distort the mean.
**Common mistakes:** Mixing windows (30 days vs 60 days) in one rate; including users who joined last week; using the wrong denominator.

### Q63 ⭐⭐ 🟡 What happens to a returned item (quality check, restock, refurbish, liquidate, destroy), and how do you measure the recovery value?
Data: 1,000 returned units worth ₹5,00,000 at selling price: 600 resold at full price, 250 resold at 50%, 150 written off. Calculate the recovery rate by value.
**Asked at:** commonly asked (no company-specific report found); reverse logistics is a gap-fill topic, no source names it (judgement).
**What the interviewer is checking:** That you follow the item to its end and measure the money recovered, not just units.
**Say this in the interview:** "After quality check, a return is restocked, refurbished, sold cheap through liquidation, or destroyed. Recovery rate by value here is 72.5%, so about 27.5% of the value is lost."
**Explain simply:**
- **Quality check:** inspect the item; grade it as new, good, damaged or unsellable.
- **Restock:** back on shelf at full price. **Refurbish:** repair or repack, sold at a discount. **Liquidate:** sold in bulk to a buyer at a deep discount. **Destroy:** hygiene or safety items that cannot be resold.
- Recovery value is measured against the original selling price (state this base; cost price gives a different rate).
**Worked example:** Average value per unit = 5,00,000 / 1,000 = ₹500.
- Full price: 600 x 500 = ₹3,00,000.
- Half price: 250 x 250 = ₹62,500.
- Written off: 150 units recover ₹0.
- Total recovered ₹3,62,500; recovery rate = 3,62,500 / 5,00,000 = 72.5%. By units, 850 of 1,000 were resold (85%), so the value rate is lower than the unit rate.
**Likely follow-ups:** 1) *Does this include return shipping cost?* Not here; a fuller view subtracts it. 2) *How to improve?* Faster QC, better grading, better liquidation buyers.
**Common mistakes:** Quoting 85% by units; mixing cost and selling price; ignoring days to resale.

### Q64 ⭐⭐ 🟡 What data and pitfalls would you consider when comparing your prices with a competitor's (pack sizes, offers, availability)?
**Asked at:** competitor-pricing scenarios were reported in a quick-commerce prep guide (claveprep snippet, unverified; page not opened).
**What the interviewer is checking:** That you compare like with like before concluding anyone is cheaper.
**Say this in the interview:** "I match products first, convert to price per unit, then compare shelf price and final price after offers, and only where both of us have stock. Otherwise the comparison misleads."
**Explain simply:**
- **Matching:** the same brand, variant and pack size. A 500 g pack and a 450 g pack are different; compare price per 100 g.
- **Offers:** compare final price after coupons, bank offers, membership discounts and delivery or handling fees, not just MRP (maximum retail price printed on the pack).
- **Availability:** a low price on an out-of-stock item is not a real price. Compare only items available to both, at the same pincode and time of day.
- **Timing and sample:** prices change several times a day; use consistent snapshots. Weight comparisons by sales, so a cheaper long-tail item does not outweigh the top sellers.
- **Data source:** scraped or purchased data can be wrong; check a sample by hand, and mind each site's terms of use.
**Data and tables involved:** `our_prices`, `competitor_snapshots` (sku match key, price, offer, stock flag, pincode, time), `product mapping`, `sales`. First cut: price index (our price over theirs) by category, sales-weighted.
**Likely follow-ups:** 1) *If we are 5% dearer, do we cut price?* Check demand sensitivity and margin first. 2) *How often to refresh?* Often for fast movers, less for slow ones.
**Common mistakes:** Comparing different pack sizes; ignoring fees and offers; including out-of-stock items; simple averages instead of sales-weighted.

### Q65 ⭐⭐ 🟡 What cost lines make up the delivery cost per order in quick commerce, and how would you calculate it?
Data (per order): base payout ₹40; surge and incentive ₹8; fuel allowance ₹4; rider insurance and support ₹2; 10% of orders need a second trip costing another ₹40 base payout. Calculate the average delivery cost per order.
**Asked at:** commonly asked (no company-specific report found); unit economics of delivery is a common quick-commerce case theme (unverified).
**What the interviewer is checking:** Whether you can build a cost per order from separate lines and handle an average that includes a minority of costly orders.
**Say this in the interview:** "Delivery cost per order is the sum of the rider's cost lines plus the expected cost of repeat trips. With these numbers it is ₹58."
**Explain simply:**
- **Base payout:** the fixed pay a rider gets for completing a delivery.
- **Surge and incentive:** extra money paid in rush hours or bad weather to attract riders, or as a target bonus.
- **Fuel allowance, insurance and support:** smaller per-order add-ons.
- **Second trip:** if the first attempt fails (customer unreachable, wrong item, rider issue), a second trip costs another base payout. Spread over all orders, it is an expected cost, not a cost every order bears.
- Real versions may add rider onboarding, uniforms or a delivery-partner fleet manager's fee; define which lines you include.
**Worked example:**
- Cost of a normal trip: 40 + 8 + 4 + 2 = ₹54.
- Second-trip cost spread over all orders: 10% x ₹40 = ₹4.
- Average delivery cost per order: 54 + 4 = **₹58**.
- Assumption: the second trip carries only the base payout, as the data states; if it also carried surge, fuel and insurance, the figure would be higher.
**Likely follow-ups:** 1) *Why not just use ₹54?* Because 1 order in 10 costs ₹94, so ₹54 understates the true average. 2) *Does it vary?* Yes, by hour, distance and weather, so report it by store and time band, not only one network number.
**Common mistakes:** Adding ₹40 for the second trip to every order; leaving out incentives because they are "not salary"; mixing a per-order cost with a per-delivery cost when some orders are batched on one trip.

### Q66 ⭐⭐ 🟡 How would you segment quick-commerce customers by monthly order frequency, and what share of GMV should each segment contribute?
Data: 1,000 customers in a month: 600 ordered 1-2 times (₹700 each), 300 ordered 3-6 times (₹2,000 each), 100 ordered 7 or more times (₹5,000 each). Calculate each segment's share of customers and of GMV.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can segment customers by behaviour and compare customer share with value share.
**Say this in the interview:** "I bucket customers by orders in the month: light, regular and heavy. Here the top 10% of customers bring about 33% of GMV, and the middle 30% bring about 39%. There is no ideal share; I judge whether the mix is healthy over time."
**Explain simply:**
- **GMV (gross merchandise value):** the total value of goods ordered, before cancellations and returns.
- Segments are a business choice; 1-2, 3-6 and 7+ orders are fine, but fix the cut-offs and keep them stable so trends are comparable.
- No target share is correct. The useful signal is the trend: are light users moving into regular, and is the company over-dependent on a few heavy users?
- Heavy users are also costly to lose; track their retention separately.
**Worked example:** (total GMV ₹15,20,000, rounded to one decimal)

| Segment | Customers | Customer share | GMV | GMV share |
|---|---|---|---|---|
| 1-2 orders | 600 | 60.0% | ₹4,20,000 | 27.6% |
| 3-6 orders | 300 | 30.0% | ₹6,00,000 | 39.5% |
| 7+ orders | 100 | 10.0% | ₹5,00,000 | 32.9% |

Heavy users are 10% of customers but 32.9% of GMV (about 3.3 times their headcount share); light users are 60% of customers but 27.6% of GMV.
**Likely follow-ups:** 1) *What else would you add?* Profit per segment, since heavy users may use more coupons. 2) *Why fixed segments?* So month-to-month movement is real, not a result of changed cut-offs.
**Common mistakes:** Quoting GMV share without customer share; forgetting that one customer can move segments each month; calling a share "right" or "wrong" without a baseline.

### Q67 ⭐⭐ 🟡 How do you define an active seller on a marketplace, and how would you measure seller churn and seller onboarding quality?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can define an entity precisely and turn it into churn and funnel metrics.
**Say this in the interview:** "I define an active seller as one with at least one delivered order in a stated window, such as the last 30 days. Churn is the share of last period's active sellers who are not active this period. Onboarding quality is how many new sellers reach their first sale and stay active."
**Explain simply:**
- **Seller:** a business that lists products on the marketplace. Definitions differ by company, so state yours: "live listing" is weaker than "had a sale".
- **Active seller:** has at least one delivered (not cancelled) order in the last 30 days. A stricter version needs a minimum number of orders.
- **Seller churn:** (sellers active last month and inactive this month) divided by (sellers active last month).
- **Onboarding quality:** a funnel: registered, documents verified, first listing live, first order, first delivered order, still active after 90 days. Also check early cancellation rate and return rate of new sellers, since a seller who sells but cancels is poor quality.
- Compare onboarding cohorts by month joined, by category and by acquisition source.
**Likely follow-ups:** 1) *Is an inactive seller a churned seller?* Not always; seasonal sellers pause. Add a "dormant for 90 days" rule. 2) *Churn is rising; what do you cut by?* Category, seller size, fees, payout delays and support tickets.
**Common mistakes:** Counting registered sellers as active; not fixing the window; measuring onboarding only by sign-ups instead of first sale and retention.

### Q68 ⭐⭐ 🟡 What are the main lines of a dark-store-level profit and loss, and how would you compare stores fairly?
**Asked at:** commonly asked (no company-specific report found); store-level profit is a common quick-commerce case theme (unverified).
**What the interviewer is checking:** Whether you know the cost structure and can avoid unfair comparisons between young and mature stores.
**Say this in the interview:** "I build the P&L from orders: revenue and margin at the top, then delivery, store and wastage costs. To compare stores fairly I use per-order figures and group stores by age and size."
**Explain simply:**
- **Dark store:** a small warehouse that only serves online orders, not walk-in customers.
- **Revenue lines:** product margin (selling price less purchase cost), delivery and handling fees, and ad or brand income.
- **Cost lines:** delivery cost (see Q65), picker and store staff pay, rent and utilities, wastage and shrinkage (spoilt, expired or lost stock), packaging, discounts funded by the company, and payment charges.
- **Contribution margin:** profit after the costs that belong to the store, before head-office cost.
- **Fair comparison:** use per-order values; compare within store-age and size groups (a store in month 2 will lose money against a mature one); look at orders per day against capacity; and treat city rent differences separately.
**Likely follow-ups:** 1) *A store has a loss; what first?* Check orders per day; low volume makes fixed costs per order high. 2) *Should head-office cost be allocated?* Show both views and say which.
**Common mistakes:** Comparing absolute profit across stores of different size; ranking new stores against mature ones; ignoring wastage.

### Q69 ⭐⭐ 🔴 How would you decide where to open the next dark store using existing order and delivery data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can turn unmet demand and delivery data into a location decision with stated assumptions.
**Say this in the interview:** "I look for areas with enough demand that is served slowly or costly by existing stores, estimate what a new store would capture, and weigh it against rent and the sales it takes from nearby stores."
**Explain simply:**
- **Demand signal:** orders per area (pincode or map grid), plus app opens with no order and "not serviceable" searches, which show demand that is lost.
- **Service quality signal:** average delivery time, late-delivery rate and rider distance per order by area; long rides mean the nearest store is too far.
- **Cannibalisation:** a new store takes orders from existing stores; subtract those from the gain, because only the net new orders count.
- **Economics:** expected orders per day against the break-even volume for one store (see Q68), plus rent and local competition.
- Shortlist areas, then rank them by net expected orders and delivery-time improvement.
**Data and tables involved:** orders (delivery location, time, store), deliveries (ride time, distance), serviceability checks, store master (location, capacity), and cost data.
**Likely follow-ups:** 1) *How do you check the forecast?* Back-test the method on stores already opened. 2) *Demand data is only for served areas; what then?* Use app opens and failed-serviceability logs.
**Common mistakes:** Picking the highest-order area (already well served); ignoring cannibalisation; using customer addresses without respecting consent and privacy rules (awareness only; from memory, unverified, confirm with the legal team).

### Q70 ⭐⭐ 🔴 A new dark store opened eight weeks ago. How would you judge whether it is ramping up well compared with older stores?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you compare like with like, using the older stores' own first eight weeks.
**Say this in the interview:** "I compare it with older stores at the same age, not with their current numbers. I line up each store's first eight weeks and look at orders, service quality and cost."
**Explain simply:**
- **Ramp-up:** how quickly a new store builds orders after opening.
- **Method:** line up older stores by "weeks since opening"; build a ramp curve (the middle store and a range, such as the middle half of stores, the 25th to 75th percentile). Plot the new store's weekly orders on it.
- **Measures:** orders per day, orders per store-hour, new customers vs repeat, delivery time, item fill rate, availability, wastage, and cost per order.
- **Adjust for context:** the opening season, the catchment size, and nearby stores. Pick comparable peers.
- **Judge:** a store below the range on orders but good on service may need marketing; a store with strong orders but high late rates needs capacity.
**Likely follow-ups:** 1) *Only eight points of data?* Yes, so be cautious; use weekly data and the range, not one number. 2) *When is it "mature"?* When weekly growth levels off, by the older stores' pattern.
**Common mistakes:** Comparing a new store to the network average today; judging on orders alone; ignoring that a store that cannibalises a neighbour has not added net demand.

### Q71 ⭐⭐ 🔴 Delivery times in a city rose sharply on rainy evenings. How would you separate the effect of rider supply, store capacity and distance, and what would you recommend?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can break one delay into stages and attribute it to the right cause.
**Say this in the interview:** "I split delivery time into stages: waiting for a rider, picking and packing, riding. Then I compare rainy evenings with dry evenings, stage by stage."
**Explain simply:**
- **Rider supply problem:** time from pick-complete to rider pick-up grows; fewer riders are logged in, or acceptance falls.
- **Store capacity problem:** time from order to pick-complete grows; orders pile up at the store, pickers are short, or the order queue is long.
- **Distance problem:** the ride stage grows, because roads are slower or orders come from farther away as nearby stores pause service.
- **Method:** compare matched time bands (rainy 7-9pm against dry 7-9pm, same weekday type) by store. A store with a long queue but idle riders points to capacity; a store with idle pickers but waiting orders points to riders.
- **Recommendations:** rain-time rider incentives, a temporary delivery-radius cut, higher delivery fee or longer promised time in heavy rain, and extra pickers.
**Data and tables involved:** order timestamps for each stage, rider logins and acceptance, store queue length, distance, and weather data by hour.
**Likely follow-ups:** 1) *Is it all rain?* Check demand: orders may also rise in the rain. 2) *How do you size the incentive?* Compare its cost with the lost orders and complaints.
**Common mistakes:** Looking only at total delivery time; ignoring demand spikes; no dry-weather comparison.

### Q72 ⭐⭐ 🔴 A membership programme (such as Prime, Flipkart VIP or Zepto Pass) claims members order more often. How would you test whether the programme caused it, given that keen buyers join more?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that correlation is not causation (selection bias) and can name a fair design.
**Say this in the interview:** "Members ordering more is expected even without any effect, because keen buyers choose to join. I would compare members with similar non-members, or better, run a randomised test."
**Explain simply:**
- **Selection bias:** the people who join already differ (they ordered more before joining), so a raw comparison overstates the effect.
- **Best option, a randomised test:** offer the programme (a free trial, say) to a random half of eligible customers; compare the offered and not-offered groups, regardless of who joined.
- **Without a test:** compare each member's orders before and after joining against a matched group of non-members (same prior orders, city, tenure), a "difference in differences" view.
- **Also check:** the cost of the benefits (free delivery, discounts) against extra margin, and whether orders are new or just shifted from other times.
**Likely follow-ups:** 1) *Why not before-and-after for members only?* Seasonality or a sale could explain it. 2) *Can you randomise?* Often yes for trials; if not, use matching and state the limits.
**Common mistakes:** Quoting the member vs non-member gap as the effect; ignoring programme cost; matching on current behaviour instead of pre-joining behaviour.

### Q73 ⭐⭐ 🔴 Item fill rate dropped from 96% to 91% in 15 of 200 stores. How would you find the cause and what would you do?
**Asked at:** commonly asked (no company-specific report found); fill rate is a quick-commerce metric in vendor material (unverified).
**What the interviewer is checking:** Whether you localise the problem across stores, products and time before offering fixes.
**Say this in the interview:** "I would check what the 15 stores share: supplier, region, categories, dates. A drop in only 7.5% of stores points to a specific cause, not a network-wide one."
**Explain simply:**
- **Item fill rate:** items delivered as ordered divided by items ordered (see Q16). A 5-point drop means more items are unavailable or cancelled.
- **Premise check:** the 5-point drop applies to those 15 stores. If the other 185 stayed at 96% and stores have equal volume, the network rate falls only to about 95.6% (computed), so the network headline can hide a real local problem.
- **Cuts:** start date of the drop; stores by city, size and age; by category and SKU; by reason code (out of stock, damaged, substituted).
- **Likely causes:** a supplier or warehouse delay serving those stores, a replenishment rule or system change, a promotion that raised demand, or a data issue such as a changed reason code.
- **Actions:** fix supply for the affected SKUs, restock priority, and raise safety stock.
**Data and tables involved:** order items (ordered and fulfilled quantity, reason), inventory snapshots, purchase orders and deliveries to stores.
**Likely follow-ups:** 1) *If all 15 share one warehouse?* Escalate to supply planning. 2) *Check the data?* Confirm the metric definition did not change.
**Common mistakes:** Averaging over all 200 stores and missing the issue; fixing symptoms before finding the date and scope.

### Q74 ⭐⭐ 🔴 How do you decide which SKUs a dark store should stock, and what data would you use to rank them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you balance sales, margin and space, not sales alone.
**Say this in the interview:** "A dark store has limited shelf space, so I rank SKUs by how much they contribute per unit of space, using sales, margin, how many customers buy them and how often they are out of stock."
**Explain simply:**
- **SKU:** a single sellable product variant (one size of one brand).
- **Rank on:** orders and units per day, contribution margin, number of distinct buyers, repeat purchase, wastage (for fresh items), and space used.
- **Local demand:** rank by store catchment; a store near offices needs different items from a residential one.
- **Roles:** some items are "traffic builders" (milk, eggs) that bring customers daily, even with low margin; keep them. Long-tail items with few buyers can be removed.
- **Account for stock-outs:** a SKU that looks slow may just have been out of stock; use sales on in-stock hours.
- Review regularly and test changes in a few stores.
**Data and tables involved:** order items, product master (size, shelf-life), inventory snapshots, costs, store catchment and cart basket data.
**Likely follow-ups:** 1) *Pareto view?* Yes, see which SKUs make most sales, but still protect traffic builders. 2) *New products?* Give a trial period with fair visibility.
**Common mistakes:** Ranking by revenue alone; ignoring stock-outs and space; copying one store's range to all.

### Q75 ⭐⭐ 🔴 Do customers who get a late delivery order less often afterwards? Describe how you would analyse it and what could mislead you.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can plan a comparison and spot confounding.
**Say this in the interview:** "I would compare the next 30 days of orders for customers with a late delivery against similar customers with an on-time delivery, and be careful that late deliveries are not random."
**Explain simply:**
- **Define:** "late" means delivered after the promised time (state the cut-off); the outcome is orders or retention in the next 30 days.
- **Compare:** take a cohort of customers in a given week; split by late or on-time first; follow their next orders.
- **Matching:** compare customers with similar past order counts, city, basket value and tenure.
- **What could mislead:** late deliveries happen in rain, at peak hours and in far areas; those customers may differ anyway. Heavy users may be more affected, or more tolerant. Customers who left are not counted if you only look at those who reorder. A customer given a refund or coupon after a late order is also changed by that.
- **Stronger evidence:** compare those late due to random causes (a rider shortage) against matched customers, or look at the size of delay: does a longer delay mean a bigger drop?
**Likely follow-ups:** 1) *Can you prove cause?* Not fully without an experiment; state the confidence. 2) *Action?* Estimate the lost value per late order and use it to decide how much to invest in speed.
**Common mistakes:** Comparing all late with all on-time customers; ignoring compensation offered; looking at average orders instead of the share who ordered again.

### Q76 ⭐⭐ 🔴 The company extended its return window from 7 to 10 days and made returns free. How would you evaluate the effect on orders, returns and margin?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you weigh extra sales against extra returns and costs, with a fair comparison.
**Say this in the interview:** "The policy has a benefit (more orders, more confidence) and a cost (more returns, return shipping). I would compare orders, return rate and contribution margin per order before and after, against a comparison group."
**Explain simply:**
- **Best design:** roll it out in some categories or cities first and keep similar ones unchanged; compare the two (a controlled test). If it was launched everywhere, use before and after with a seasonal adjustment.
- **Orders:** orders, conversion and new customers, per category.
- **Returns:** return rate by orders and by value (Q13); timing of returns (many in days 8-10 show the longer window is used); return reason; share of returns that can be resold.
- **Margin:** gross margin less delivery cost, less return shipping and handling, less value lost on unsellable items, per order.
- **Verdict:** extra margin from additional orders compared with the extra return cost. Look by category: fashion may react very differently from electronics.
- **Watch:** serial returners and "wardrobing" (use then return).
**Likely follow-ups:** 1) *Short-term jump?* Check after returns settle; the cost shows late. 2) *Which category first?* Where return costs are low and resale high.
**Common mistakes:** Looking at orders only; measuring returns before the full window has passed; ignoring seasonality.

### Q77 ⭐ 🟢 What is a private label on an e-commerce platform, and why do platforms track its share of GMV and margin?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand why a platform sells its own brand.
**Say this in the interview:** "A private label is a product sold under the platform's own brand, made by a third party. Platforms track it because it usually earns a higher margin than other sellers' products, and it can fill gaps in the range."
**Explain simply:**
- **Private label:** the platform (or a related company) owns the brand and has a manufacturer make it, for example a house brand of grocery staples or basic clothing.
- **Share of GMV:** the portion of total order value from these products; shows how much of sales relies on it.
- **Margin:** the platform keeps the full product margin, instead of only a commission from a seller.
- **Care points:** rules or regulators may look at a platform favouring its own brand in search or promotion (from memory, unverified, confirm with the legal team). Analysts should track fairness metrics, such as search rank, and customer ratings and return rates for private label items.
**Likely follow-ups:** 1) *Is a higher share always good?* No; quality issues or seller conflict can hurt. 2) *Measure?* Margin per unit, return rate, repeat purchase.
**Common mistakes:** Looking at GMV share without margin; comparing with branded items without controlling for price tier.

### Q78 ⭐ 🟢 What is the buy box on a marketplace, and why do sellers care about it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know how one product page can have many sellers and how one wins most sales.
**Say this in the interview:** "The buy box is the default seller offer behind the main buy button. Sellers care because most purchases go through it."
**Explain simply:**
- When several sellers sell the same product, the page shows one seller's offer by default: the "buy" or "add to cart" button.
- The platform picks it with its own mix of factors, such as price including delivery, delivery speed, seller rating and stock; exact rules are not public (from memory, unverified).
- Sellers who win it get far more orders for the same product; others appear under "other sellers".
- Analyst metrics: **buy box win rate** (share of page views or time where the seller holds it), orders by offer, price gap to the winner, and the share of GMV going to the winning seller.
**Likely follow-ups:** 1) *A seller lost it; why?* Check price, delivery time, stock-outs, rating changes. 2) *Can a seller just cut price?* That may lose margin; track profit, not only wins.
**Common mistakes:** Treating it as a pure price contest; ignoring stock and delivery speed.

### Q79 ⭐ 🟡 In plain words, what do the Consumer Protection (E-Commerce) Rules and the dark-pattern guidelines mean for an analyst working on checkout, pricing and COD fees?
**Asked at:** commonly asked (no company-specific report found); regulation topics are a differentiator rather than a staple (unverified).
**What the interviewer is checking:** Awareness that checkout and pricing analysis must stay honest and transparent.
**Say this in the interview:** "I am not a lawyer, but as I understand it, the rules aim at fair, clear dealings with customers: no hidden charges, no tricking people into choices. I would check design and pricing ideas with the compliance team."
**Explain simply:**
- Everything here is from memory, unverified, and awareness only; confirm with the compliance or legal team.
- **Consumer Protection (E-Commerce) Rules:** as I recall, they require platforms to show clear prices, seller details and a grievance process, and to deal fairly with customers. Check the current text and amendments.
- **Dark patterns:** design tricks that push customers into choices they did not intend, as I recall, such as hidden charges added at the last step, fake urgency ("only 2 left!") or a pre-ticked add-on.
- **Analyst impact:** an experiment that raises conversion by hiding a fee might be a dark pattern, not a win. Show the total price early; document tests; track complaints and refund requests as well as conversion.
- **COD fees:** whether a separate COD charge is covered is something I would ask legal; disclose it clearly in any case.
**Likely follow-ups:** 1) *What would you do if a test raises sales through hidden fees?* Raise it with product and legal. 2) *Which metric guards this?* Complaints, cancellations after the last step.
**Common mistakes:** Treating conversion as the only goal; claiming legal facts with certainty.

### Q80 ⭐ 🟡 Does GMV include GST and delivery fees, and why does the answer matter when you compare with finance numbers?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you check metric definitions before comparing two reports.
**Say this in the interview:** "It depends on the company's definition, so I ask. Some include tax and delivery fees, others do not. Finance usually reports revenue after removing GST, so the two numbers differ even when both are correct."
**Explain simply:**
- **GMV (gross merchandise value):** total value of orders placed. Definitions differ across companies; I state mine.
- **GST (goods and services tax):** a tax collected for the government, so it is not the company's income; finance revenue normally excludes it.
- **Delivery and other fees:** may be in GMV or not, and may be revenue for the company or a pass-through to someone else.
- **Other differences:** cancellations and returns (GMV is often before them), timing of order versus delivery, and discounts.
- **Method:** list the definition of each, reconcile step by step, and show a bridge from GMV to finance revenue.
**Worked example:** (invented figures; GST rate of 18% is only for the exercise)
- Item price before tax ₹1,000; GST ₹180; delivery fee ₹40.
- Customer pays ₹1,220.
- GMV definitions: with everything ₹1,220; with GST, without delivery ₹1,180; without GST, with delivery ₹1,040; item only ₹1,000.
- Same order, four different "GMV" values. Gaps between reports of ₹180 or ₹40 per order are definitions, not errors.
**Likely follow-ups:** 1) *Which is correct?* All are, if labelled; pick one for dashboards and state it. 2) *How do you reconcile with finance?* Build the bridge: GMV, less tax, less cancellations and returns, plus or minus timing.
**Common mistakes:** Comparing numbers without checking definitions; forgetting the tax; calling the gap a data error.

### Q81 ⭐ 🟡 What does a marketplace settlement report show (orders, commission, fees, returns, payout), and how would you reconcile it with the orders table?
**Asked at:** commonly asked (no company-specific report found); settlement and payout reconciliation is a finance-ops topic, not named in the sources file.
**What the interviewer is checking:** Whether you understand that a seller is paid net of deductions, and can match two data sources row by row.
**Say this in the interview:** "A settlement report is the marketplace's pay slip to a seller. For each order it shows sale value minus commission, fees and return deductions, giving the payout. I reconcile by joining it to the orders table on order ID and flagging missing, extra and mismatched rows."
**Explain simply:**
- **Settlement report:** a periodic statement (often weekly) of what the platform owes a seller. Think of payroll: gross pay, deductions, net pay, one line per employee; here one line per order.
- **Commission:** the platform's percentage cut of the sale. **Fees:** fixed charges such as shipping or payment handling. **Return deduction:** money taken back when the customer returns the item.
- **Payout:** the net amount transferred to the seller's bank account.
- Reconciliation asks three things: is every delivered order paid, is every paid order a real order, and does each payout equal value minus deductions?
**Worked example:** (invented data; payout rule used: payout = item value - commission - fees)
```sql
-- Compare each order with its settlement line and label the result
select o.order_id, o.status, o.item_value, s.payout,
       case
         when s.order_id is null and o.status = 'delivered' then 'delivered, not settled'
         when s.order_id is null then 'not settled (expected)'
         when s.payout <> o.item_value - s.commission - s.fees then 'payout mismatch'
         else 'ok'
       end as check_result
from orders o
left join settlement s on s.order_id = o.order_id;
-- second query: settlement lines with no matching order
select s.order_id, s.payout from settlement s
where s.order_id not in (select order_id from orders);
```
Output: O1 ok; O2 payout mismatch (expected 500-75-40 = 385, paid 395, so 10 overpaid); O3 ok; O4 delivered, not settled (600 unpaid); O5 not settled, expected (cancelled); second query shows O6 with payout 470 and no order behind it.
Plain words: one order is overpaid by 10, one delivered order is unpaid, and one payout has no order behind it, all to be raised with finance.
**Data and tables involved:** orders, settlement lines, returns, and the commission rate card; first cuts are total value vs total payout by week, and count of unmatched rows.
**Likely follow-ups:** 1) *Why might delivered orders be missing?* Payout timing (paid after a return window), so compare using the settlement cycle. 2) *Which key do you join on?* Order ID, or order-item ID if one order has several sellers.
**Common mistakes:** Joining only one way and missing extra settlement rows; ignoring timing; comparing cancelled orders that were never meant to be paid.

### Q82 ⭐ 🟡 What is a delivery slot or cut-off time (same-day, next-day, scheduled), and how would you analyse its effect on orders and cost?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can link an operational rule (a deadline) to customer behaviour and cost.
**Say this in the interview:** "A cut-off time is the last moment an order can be placed to qualify for a delivery promise, for example order before 2 pm for same-day. I would compare orders, conversion, late rate and cost per order across slots."
**Explain simply:**
- **Same-day:** delivered the day it is ordered, only if placed before the cut-off. **Next-day:** delivered the following day. **Scheduled:** the customer picks a date or time window.
- Cut-offs exist because pickers, trucks and riders work in fixed waves. An order just after the cut-off waits for the next wave.
- Faster slots usually cost more per order (less batching, more rush staffing); scheduled slots let the platform batch orders and cut cost.
- Analysis: orders by hour with the cut-off marked; conversion by slot offered; on-time rate and cost per order by slot; share of orders landing just before the cut-off (a pile-up means pressure on pickers).
**Likely follow-ups:** 1) *How do you judge if moving the cut-off helps?* Pilot in some pincodes and compare to similar ones. 2) *What spikes just before the cut-off?* Orders and picker workload, so late risk rises.
**Common mistakes:** Looking at order volume only and ignoring cost and lateness; forgetting that customers who see no same-day option may simply not order.

### Q83 ⭐ 🟡 In plain words, what is the gig-worker social security provision in India, and why do analysts need to treat rider pay and location data with care?
**Asked at:** commonly asked (no company-specific report found); awareness topic, thinly evidenced.
**What the interviewer is checking:** Awareness that people data carries legal and ethical duties; no legal expertise is expected.
**Say this in the interview:** "As I understand it, India's social security law now recognises gig and platform workers such as delivery riders, and platforms are expected to contribute to a welfare fund. Rider pay and live location are personal data, so I use the minimum, aggregate where possible, and follow the company's compliance guidance."
**Explain simply:**
- **Gig worker:** someone paid per task (per delivery), not a monthly salary. Traditionally they had no provident fund or insurance cover like an employee.
- The provision, **from memory, unverified**: the Code on Social Security, 2020 names gig and platform workers and asks aggregators (platforms) to contribute a small percentage of their turnover, with a cap tied to what they pay workers, into a social security fund. Rules, rates and start dates are for the legal team to confirm.
- For analysts this means rider records (earnings, hours, ID) may feed benefit calculations, so accuracy matters; an HR analyst will see this resembles payroll accuracy.
- **Care with data:** pay is sensitive, and location data can reveal where a person lives or spends time. Under India's data protection law (from memory, unverified) personal data should be used for a stated purpose with consent and kept only as long as needed.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team. No legal advice.
**Likely follow-ups:** 1) *Would you share rider-level pay in a dashboard?* No; show city or store averages. 2) *Can you track riders' GPS?* For operations yes, but limit access and retention.
**Common mistakes:** Quoting exact rates or dates as fact; exporting rider names and phone numbers into open spreadsheets; treating riders as employees in headcount reports without checking definitions.

### Q84 ⭐ 🟡 How would you plan seasonal workforce for a fulfilment centre ahead of a festive sale, using last year's orders and productivity data?
**Asked at:** commonly asked (no company-specific report found); workforce questions are gap-fill (HR-flavoured) in the sources file.
**What the interviewer is checking:** Whether you can turn a demand forecast into a headcount number with explicit assumptions, an HR-friendly skill.
**Say this in the interview:** "I take last year's peak daily orders, scale by expected growth, divide by orders handled per person per shift, then add a buffer for absence, and subtract current staff to get the hiring need."
**Explain simply:**
- **Fulfilment centre (FC):** a large warehouse where items are picked, packed and handed to couriers.
- **Productivity:** orders one packer handles in a shift (e.g. 90). Use last year's actual data, split by new vs experienced staff, since seasonal hires are slower in week one.
- **Buffer:** absenteeism and attrition spike in festive weeks, so plan on staff who show up, not staff on roll.
- **Steps:** peak day demand, growth assumption, people needed, absence uplift, minus existing, then time hiring and training before the sale.
**Worked example:** (invented inputs) last year's peak 40,000 orders/day; expected growth 25%; productivity 90 orders per packer per shift; absence 8%; 450 permanent packers (one-shift view).
- Peak demand = 40,000 x 1.25 = 50,000 orders.
- Packers on floor = 50,000 / 90 = 555.6, round up 556.
- On roll after 8% absence = 555.6 / 0.92 = 603.9, round up 604.
- Seasonal hires = 604 - 450 = 154.
Plain words: hire about 154 temporary packers; a second shift or lower new-joiner productivity would change this.
**Likely follow-ups:** 1) *What if growth is uncertain?* Run low, base and high cases. 2) *What else?* Pickers, loaders, supervisors, and training capacity.
**Common mistakes:** Planning on average days instead of the peak; ignoring absence and ramp-up; forgetting onboarding lead time.

### Q85 ⭐ 🟡 Why are product ratings and reviews biased, and how would you use them in an analysis?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you question data that looks objective but comes from a self-selected group.
**Say this in the interview:** "Reviews come only from people who chose to write one, so they are not a random sample. I use ratings as a signal alongside returns and repeat purchase, never alone."
**Explain simply:**
- **Self-selection bias:** very happy and very angry customers review; the satisfied middle stays silent. Ratings often look U-shaped or skewed high.
- **Purchase bias:** people who disliked a product often return it and never review.
- **Incentives and fakes:** free-product reviews, seller-arranged reviews and review bombing distort scores.
- **Small counts and timing:** a 4.8 from 5 reviews is weaker than 4.5 from 5,000; old reviews may describe an old version.
- **Using them well:** show rating with review count; compare against return rate and complaints; analyse review text themes (size, quality); weight verified-purchase reviews.
**Likely follow-ups:** 1) *How compare two sellers?* Set a minimum number of reviews, or pull a seller with few reviews toward the overall average before comparing. 2) *Does rating drive sales?* It correlates, but better products get both.
**Common mistakes:** Averaging stars as if they were measurements; ignoring the count; treating correlation as cause.

### Q86 ⭐ 🟡 What dashboard or data would a brand or seller want from a marketplace, and which of it can the platform share?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can separate useful business data from data that must stay private.
**Say this in the interview:** "A seller wants sales, stock, returns, ads and customer-experience metrics for their own products. The platform can share aggregated data about the seller's own business, but not personal customer details or competitors' data."
**Explain simply:**
- **Seller wants:** orders, units and revenue by product; conversion (visits that became orders); return rate and return reasons; stock and stockouts; ad spend and results; ratings; settlement and payout summary; search ranking and delivery performance.
- **Brand wants more on market view:** category share, price position, search terms (aggregated).
- **Can usually share:** the seller's own transactions, aggregated trends, city-level or pincode-group demand.
- **Should not share:** customer names, phone numbers and addresses (beyond what is needed to ship), other sellers' sales or prices, internal ranking formulas. Privacy law and platform contracts apply (from memory, unverified, confirm with legal).
**Likely follow-ups:** 1) *Why aggregate?* Small counts could identify a customer. 2) *Self-serve or reports?* A self-serve dashboard with fixed definitions.
**Common mistakes:** Sharing raw customer rows; changing metric definitions between reports; showing competitor benchmarks that reveal rivals.

### Q87 ⭐ 🟡 What is item substitution in quick commerce, and how would you measure substitution acceptance?
**Asked at:** commonly asked (no company-specific report found); fill-rate vocabulary appears in quick-commerce vendor blogs (unverified).
**What the interviewer is checking:** Whether you can define a rate with the right denominator and see why it matters.
**Say this in the interview:** "Substitution means offering a similar item when the ordered one is out of stock. Acceptance rate is accepted substitutions divided by substitutions offered."
**Explain simply:**
- **Quick commerce:** groceries delivered in minutes from a **dark store** (a small warehouse closed to the public).
- A picker finds an item missing; the app proposes a replacement (a different brand or size). The customer accepts or declines, or the picker substitutes automatically.
- **Measure:** offered rate (of orders with a stockout), acceptance rate, and outcome (item removed, refund, order cancelled).
- Segment by category, price gap between original and substitute, and whether the customer was asked first.
**Worked example:** (invented) 1,000 orders had a missing item; 300 got a substitution offer; 210 accepted, 60 declined, 30 no response.
- Offer rate = 300 / 1,000 = 30%.
- Acceptance rate = 210 / 300 = 70%.
- Accepted per stockout order = 210 / 1,000 = 21%.
Plain words: 70% accept when asked, but only 30% of affected orders are even offered a substitute, so offering more often is the bigger lever.
**Likely follow-ups:** 1) *Is high acceptance always good?* Not if auto-substituted and later returned. 2) *Denominator?* Say which one you use.
**Common mistakes:** Mixing offered and total orders; ignoring no-response; ignoring later returns of substitutes.

### Q88 ⭐ 🟡 What is a damaged-in-transit rate, and how would you split it between packaging, courier and handling?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can isolate causes by splitting data in more than one way.
**Say this in the interview:** "Damaged-in-transit rate is damaged shipments divided by shipments delivered. To find the cause I split by courier, packaging type, product category and warehouse, and check them together because they overlap."
**Explain simply:**
- Define damage by customer claim or return reason; this undercounts silent damage.
- **Packaging:** box type, bubble wrap, fragile category. **Courier:** damage by partner, route, pincode zone. **Handling:** warehouse packer, shift, loading.
- Causes overlap: a courier might look bad only because it carries more unpackaged goods.
**Worked example:** (invented)
| Courier | Packaging | Shipments | Damaged | Rate |
|---|---|---|---|---|
| X | bubble | 1,000 | 10 | 1.0% |
| X | plain | 200 | 10 | 5.0% |
| Y | bubble | 200 | 2 | 1.0% |
| Y | plain | 600 | 24 | 4.0% |
Overall 46 / 2,000 = 2.3%. By courier: X 20/1,200 = 1.7%, Y 26/800 = 3.25%, so Y looks worse. By packaging: bubble 12/1,200 = 1.0%, plain 34/800 = 4.25%. Within each packaging type the couriers are similar (1.0% vs 1.0%; 5.0% vs 4.0%): packaging, not courier, drives most damage.
**Likely follow-ups:** 1) *Next step?* Pilot bubble wrap on plain orders. 2) *Cost?* Compare packaging cost to damage cost.
**Common mistakes:** Blaming the courier from one split; ignoring unreported damage.

### Q89 ⭐ 🟡 Why are price experiments tricky in e-commerce, given that customers compare prices across apps?
**Asked at:** commonly asked (no company-specific report found); price-undercut scenarios appear in a quick-commerce prep blog snippet (unverified).
**What the interviewer is checking:** Whether you see why a simple A/B test can mislead when customers shop around.
**Say this in the interview:** "Customers compare prices across apps, so a price test can change who shows up, not just how they react. I would test carefully, track spillover, and look at margin and repeat behaviour, not just conversion."
**Explain simply:**
- **Price experiment:** show different prices to similar customers, compare orders and profit.
- **Problems:** customers can see differing prices on other devices or social media (fairness and trust); competitors react; products are substitutes, so lowering one price pulls sales from another; sales spike then dip as buyers stock up.
- **Design:** randomise by store or pincode, keep tests short, track units, margin, basket size and 30-day repeat.
- Fairness: personalised pricing can look unfair, and consumer protection rules may apply (from memory, unverified).
**Likely follow-ups:** 1) *Metric?* Profit per visitor, not conversion. 2) *Store-level or user-level?* Store-level cuts leakage between customers.
**Common mistakes:** Judging by revenue alone; ignoring competitors and seasonality; reading a short sale spike as lasting.

### Q90 ⭐ 🔴 Do faster delivery estimates raise conversion? Describe how you would analyse it and what could mislead you.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Causal thinking: correlation versus cause.
**Say this in the interview:** "I would not just compare pincodes with fast and slow estimates, because they differ in other ways. I would compare like with like, and ideally run a controlled test."
**Explain simply:**
- **Delivery estimate:** the date or minutes shown on the product page. **Conversion:** share of visits that turn into orders.
- **Naive view:** fast-estimate pages convert better. That may be because fast estimates appear in dense metro areas, for in-stock popular items, with richer customers.
- **Analysis steps:** compare within the same city, category and price band; control for stock and time of day; use before/after with a comparison group; best, a randomised test showing different estimates to similar users (ethically, only changing the display of true promises).
- **What can mislead:** confounders (other differences that move both delivery estimate and buying), promises that cause later late-delivery complaints, short windows, and effects that show in repeat purchase and returns rather than first conversion.
**Likely follow-ups:** 1) *Better metric?* Conversion and on-time rate together. 2) *Test cell?* Pincodes or users.
**Common mistakes:** Comparing metro against rural; treating a correlation as a lift; ignoring failed promises.

### Q91 ⭐ 🔴 Design a seller scorecard for a marketplace: which metrics, what weights, and how would you avoid unfair penalties?
**Asked at:** commonly asked (no company-specific report found); seller scorecard design is a differentiator for product companies.
**What the interviewer is checking:** Whether you can turn judgement into transparent weights and think about fairness.
**Say this in the interview:** "I pick a small set of metrics that sellers control, weight them by customer impact, compare sellers with peers in the same category and enforce minimum volumes so small samples are not punished."
**Explain simply:**
- **Metrics (illustrative weights, a design choice):** on-time dispatch 25%, order defect or cancellation rate 25%, return rate for seller-fault reasons 20%, rating 15%, wrong or damaged item claims 15%. Total 100%.
- **Fairness:** count only seller-fault outcomes; compare within category (apparel returns exceed grocery); set a minimum number of orders; show trends and give a warning period; allow appeals; exclude courier or festive disruption.
- **Score:** convert each metric to 0 to 100 against category peers, multiply by weight, add up.
- Show the formula to sellers.
**Likely follow-ups:** 1) *High-GMV poor seller?* Coach, then restrict listing, not an instant ban. 2) *How to validate?* Check the score predicts later complaints.
**Common mistakes:** Penalising for courier delays; mixing categories; opaque weights; no minimum volume.

### Q92 ⭐ 🔴 Late-night orders in quick commerce are few. How would you decide whether a dark store should shorten its opening hours?
**Asked at:** commonly asked (no company-specific report found); store-economics questions are gap-fill.
**What the interviewer is checking:** Whether you weigh incremental profit against fixed cost and customer effects.
**Say this in the interview:** "I compare the contribution from late-night orders with the cost of staying open, then check how many customers I would lose in the daytime if the store closed."
**Explain simply:**
- **Contribution per order:** order value x margin minus variable cost such as rider payout.
- **Fixed night cost:** staff, power, rider standby, wastage.
- Also count **halo effect**: customers who order at night may also be loyal daytime users.
**Worked example:** (invented) average order Rs 350; 20% margin; rider cost Rs 30 per order; three staff for four hours at Rs 120 per hour; 14 orders per night.
- Contribution per order = 350 x 0.20 - 30 = Rs 40.
- Night fixed cost = 3 x 4 x 120 = Rs 1,440.
- Break-even = 1,440 / 40 = 36 orders.
- Actual = 14 x 40 = Rs 560, a loss of Rs 880 per night.
Plain words: the store needs 36 night orders to break even, so shorten hours unless the halo or strategic value covers Rs 880.
**Data needed:** hourly orders, staffing roster, margins, repeat behaviour of night customers.
**Likely follow-ups:** 1) *Alternative to closing?* Fewer staff, a reduced assortment or a shared store. 2) *Test?* Shorten hours in a few stores.
**Common mistakes:** Using averages across all hours; ignoring halo and brand; counting fixed costs that do not go away.

### Q93 ⭐ 🔴 How would you design an RTO risk score for COD orders, which inputs would you use, and how would you check it does not unfairly block good customers?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Risk modelling plus fairness: you should not block good customers.
**Say this in the interview:** "I would estimate each COD order's chance of RTO from past data and use the score to choose a light action such as a confirmation call or prepaid nudge, not an outright block, and measure how many good customers are affected."
**Explain simply:**
- **COD:** cash on delivery. **RTO:** return to origin, the parcel comes back undelivered.
- **Inputs:** customer's past delivery and RTO history, order value, pincode RTO rate, product category, order time, address quality, number of recent orders; use history as input, not personal traits.
- **Method:** a simple rule-based score or a basic model (logistic regression, which turns the inputs into a probability between 0 and 1), built on past orders and tested on later months.
- **Fairness check:** see how many good customers (delivered) are flagged, and check results by region.
**Worked example:** (invented) 1,000 COD orders, 200 end in RTO (20%). Threshold flags 150 orders: 90 RTO and 60 delivered.
- Precision (of the orders flagged, how many really became RTO) = 90 / 150 = 60%.
- Recall (of all RTOs, how many we caught) = 90 / 200 = 45%.
- Good customers flagged = 60 / 800 = 7.5%.
Plain words: at this threshold 45% of RTOs are caught but 7.5% of good customers are flagged, so use a call, not a block.
**Likely follow-ups:** 1) *Threshold?* Pick by cost: RTO cost vs lost sale. 2) *Monitor?* Re-check monthly.
**Common mistakes:** Blocking outright; evaluating on training data; using proxies for protected traits.

### Q94 ⭐ 🔴 City A shows a better on-time delivery rate than city B overall, but B is better in every order-type segment. How can that happen, and how would you report it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know Simpson's paradox: an overall number reversing when a hidden mix is ignored.
**Say this in the interview:** "The overall rate is a weighted average of segment rates, so it depends on the mix of orders. City A can look better simply because it has more easy standard orders. I would report segment rates and a mix-adjusted comparison."
**Explain simply:**
- **On-time rate:** on-time deliveries divided by total deliveries. **Segment:** standard or express.
- Express is harder to deliver on time, so a city with many express orders drops overall.
**Worked example:** (invented, 1,000 orders per city)
| City | Standard orders | Standard on time | Express orders | Express on time | Overall |
|---|---|---|---|---|---|
| A | 900 | 90% | 100 | 60% | 87.0% |
| B | 100 | 92% | 900 | 65% | 67.7% |
- A: (810 + 60) / 1,000 = 87.0%. B: (92 + 585) / 1,000 = 67.7%.
- B is better in standard (92% vs 90%, 2 percentage points) and express (65% vs 60%, 5 points), yet 19.3 points lower overall, because 90% of B's orders are express.
- Fair comparison: apply the same mix to both cities (standardisation).
**Likely follow-ups:** 1) *Which to report?* Segments, plus a mix-adjusted overall. 2) *Other examples?* Attendance by department.
**Common mistakes:** Reporting only the overall rate; calling A better; mixing percentage and percentage points.

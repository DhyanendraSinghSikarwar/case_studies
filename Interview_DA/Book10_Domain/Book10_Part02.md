# Book 10 — Domain Knowledge | Part 2: E-commerce & Quick-commerce 🟢🟡🔴

**Target:** 90 questions | **Actual:** 80 questions
**Scope:** how e-commerce and quick-commerce work (orders, GMV, AOV, conversion, returns, RTO, delivery SLAs, dark stores, catalogue, marketplace sellers, payments), their data tables and domain metrics, plain-words privacy awareness and domain analysis tasks.

### Q1 ⭐⭐⭐ 🟢 How does an online marketplace such as Flipkart or Amazon make money, and how is that different from an inventory-led e-commerce retailer and from a quick-commerce company such as Blinkit, Zepto or Swiggy Instamart?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Walk me through the life of an e-commerce order, from the customer pressing "place order" to delivery or return, and name the data you get at each stage.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is the difference between a cancellation, a customer return and an RTO (return to origin) in Indian e-commerce, and why does an analyst track them separately?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is a SKU, and how is it different from a product, a listing and a seller offer on a marketplace?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is a dark store, and how is it different from a normal supermarket and from a fulfilment centre or warehouse?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What does a "10-minute delivery" promise contain, and which time stages (order to pick-complete, pick-complete to rider pick-up, ride, handover) does an analyst measure?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 Why does cash on delivery (COD) matter so much to an Indian e-commerce analyst, and how does it change the metrics you track?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 Which tables would you expect in an e-commerce database (customers, orders, order items, products, payments, shipments, returns), and how do they connect to each other?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 What is the difference between order-level data and order-item-level data, and how does mixing them give wrong order counts or wrong shipping-fee totals?
Data: order 101 has a shipping fee of ₹40 in the orders table and three rows in the order-items table (₹300, ₹200 and ₹100). If you join the two tables and sum the shipping fee, what total do you get for this one order, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Walk through the waterfall from gross GMV to net sales after cancellations, RTO and customer returns, and explain why leadership may still quote the gross number.
Data (one month, ₹ crore): gross GMV 100; cancelled before shipping 8; RTO 6; returned after delivery 12. Calculate net delivered sales and each loss as a share of gross GMV.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 How do you calculate the on-time delivery rate, and how does the choice of denominator change the answer?
Data (one week): 10,500 shipments had a promised delivery date in the week; 8,700 were delivered on or before the promised date; 1,300 were delivered late; 500 are still undelivered and past the promised date. Calculate the on-time rate on all due shipments and on delivered shipments only.
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 What is the return rate, and how does it differ when you measure it by orders, by units and by value?
Data (January): 50,000 orders delivered with 60,000 units worth ₹3 crore. Returned: 6,000 units from 4,500 orders worth ₹40 lakh. Calculate the return rate by orders, by units and by value.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you tag a customer as new or repeat from an orders table, and what goes wrong with guest checkouts, duplicate accounts and a cancelled first order?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Which metrics would a marketplace use to judge a seller's performance, and what would you do about a seller with high GMV but poor metrics?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 What is the difference between order fill rate and item fill rate in quick commerce, and why do both matter?
Data (one store, one day): 1,000 orders containing 4,000 items. 3,760 items were delivered; 180 orders had at least one item missing. Calculate the item fill rate and the order fill rate.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Which data and tables would you need to build a daily dashboard for a dark store manager, and which first cuts would you show?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 What is on-shelf availability (or stock-out rate) in quick commerce, and how would you measure it from hourly stock snapshots?
Data: a store lists 2,000 SKUs and is snapshotted for 14 hours a day. Total in-stock SKU-hours were 25,200. Calculate the availability, and say why a demand-weighted figure can differ.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 How would you analyse payment failure at checkout, and which payment methods and stages would you compare?
Data (one day, attempts / successes): UPI 70,000 / 63,000; cards 20,000 / 17,000; netbanking 5,000 / 4,000. Calculate the success rate by method and overall, and say why attempts and unique orders are not the same.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 An orders table holds several status rows per order (placed, packed, shipped, delivered). How do you pull the latest status per order, and how is a status-history table different from a snapshot table?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 What is a monthly transacting user (MTU) and why do e-commerce and quick-commerce companies prefer it to registered or installed users?
Data: 30 lakh orders in a month from 12 lakh transacting users and 80 lakh registered users. Calculate orders per MTU and the share of registered users who transacted.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐⭐ 🟡 You are asked to build the daily MIS report for an e-commerce operations team. Which columns, views and ageing buckets would you include for orders received, packed, shipped, delivered and pending?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐⭐ 🔴 The return rate in women's ethnic wear rose from 18% to 27% in six weeks. Which data cuts would you run to find the cause?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐⭐ 🔴 Late deliveries in Hyderabad rose from 8% to 15% of shipments. Which data cuts would you use to isolate the cause?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐⭐ 🔴 COD orders show a much higher RTO rate than prepaid orders. Use the data to decide whether a confirmation-call programme is worth running, and say what else you would test.
Data (one month): 40,000 COD orders with 14% RTO; 60,000 prepaid orders with 3% RTO. Each RTO costs ₹90 in forward and reverse shipping. A confirmation call costs ₹5 per COD order and is expected to cut COD RTO to 10%.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 What are the main fulfilment models in e-commerce: seller-fulfilled, platform-fulfilled (such as Fulfilled by Amazon or Flipkart Assured) and inventory-led, and how do they change the data you see?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 What are forward logistics and reverse logistics, and what do first mile, mid mile, last mile, a courier partner (3PL) and a pincode zone mean?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 Which metrics spike during a festive sale such as Big Billion Days or the Great Indian Festival, and how should an analyst compare it with a normal period?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 Why do platforms charge a delivery fee, handling fee, small-cart fee or minimum order value, and which metrics tell you whether these fees work?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 What are the common reasons for cancellations (customer, seller, system, payment, stock-out), and which reasons would you want to reduce first?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 What is serviceability in e-commerce and quick commerce, and how is pincode or geofence coverage data used?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 A seller sells a ₹1,000 item. Calculate the seller payout and the platform's take rate from the fees below, and say which fees are commonly charged by marketplaces.
Data: commission 12%, fixed closing fee ₹20, shipping fee ₹60, collection fee 2% of price. Ignore GST.
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 What are ROAS and ACoS for sponsored listings on a marketplace, and how do ad revenues fit into platform revenue?
Data: a brand spent ₹50,000 on sponsored listings and the ads were credited with ₹4,00,000 of sales. Calculate ROAS and ACoS.
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How do you measure on-site search quality, and what is the zero-result or null-search rate?
Data (one day): 2,00,000 searches; 12,000 returned no results; 30,000 searches ended in an order. Calculate the null-search rate and the search-to-order rate.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How would you use the 80/20 (Pareto) view on SKUs and categories, and what decisions does it support?
Data: a category has 1,000 SKUs; the top 100 give 62% of GMV and the bottom 500 give 4%. What would you check before you delist the tail?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 What is the difference between MRP, selling price, discount percentage and effective price after bank offers, and why can an average discount mislead?
Data: a phone has an MRP of ₹20,000 and a selling price of ₹15,000, plus a ₹1,000 bank offer. Calculate the headline discount and the effective discount.
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How would you test whether a discount coupon created extra orders rather than just discounting orders that would have happened anyway?
Data: 10,000 customers got a ₹75 coupon and placed 25,000 orders, all using the coupon. A similar control group of 10,000 customers got no coupon and placed 20,000 orders. Calculate incremental orders and coupon cost per incremental order.
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Who funds a discount on a marketplace (seller, brand or platform), and why does it matter for net revenue and margin?
Data: MRP ₹1,000; selling price ₹800. The seller funds ₹100 of the discount and the platform funds ₹100.
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 What is a contact rate in customer support, and which reason tags (for example "where is my order") would you analyse first?
Data: 2,50,000 orders and 15,000 support tickets in a week; 6,000 tickets were "where is my order". Calculate the contact rate per 100 orders and the share of such tickets.
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 What are first-attempt delivery rate and an NDR (non-delivery report), and how do they drive RTO?
Data: 20,000 shipments; 17,000 delivered on the first attempt; 2,500 raised an NDR, of which 1,000 were delivered on re-attempt; the rest returned to origin. Calculate the first-attempt rate and the RTO count.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 How do you measure delivery-partner productivity and cost, and which numbers would you show a city operations head?
Data (one rider-day): 8 hours logged in, 2 hours idle, 20 orders delivered, ₹1,200 total pay and incentives. Calculate orders per logged-in hour, orders per active hour and cost per order.
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Which workforce metrics (attendance, shift fill, productivity per picker hour, attrition) would you track for dark store pickers and delivery partners, using your HR background?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 Your platform onboards delivery partners. How would you analyse the onboarding funnel and where would you look for drop-off?
Data (one month): 10,000 applied; 6,000 documents verified; 4,500 trained; 3,600 took a first order; 2,000 still active after 30 days. Calculate step-wise and overall conversion.
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 How would you tell the difference between wastage (known losses) and shrinkage (unexplained loss) for a fresh category in a dark store?
Data: 5,000 kg of produce received; 4,500 kg sold; 300 kg recorded as expired or damaged; the rest unaccounted for. Calculate the wastage, shrinkage and total loss percentages.
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 How do items per order and AOV together explain a change in basket size, and what would you check?
Data: week 1 had 10,000 orders and 32,000 items; week 2 had 11,000 orders and 40,700 items. Calculate items per order for each week and say what could explain the change.
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 What is the minimum AOV at which a quick-commerce order breaks even on contribution, given the cost lines below?
Data per order: gross margin 18% of AOV; ads income ₹10; pick-and-pack ₹25; last-mile delivery ₹45; payment and other costs ₹10; allocated store cost ₹15.
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 How do you connect app or web session events (clickstream) to orders, and what attribution problems arise?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 How is a session defined on an app or website, and why can session counts differ between a web-analytics tool and your own event data?
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 What does a catalogue analyst check (duplicate listings, missing attributes, wrong categories, poor images), and how does bad catalogue data affect conversion and returns?
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 Which fraud and abuse patterns appear in e-commerce (coupon abuse, return fraud, fake COD orders, refund abuse), and what data would flag them?
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 Which date do you use to report an order to a month: order date, payment date, dispatch date or delivery date, and how does the choice change the numbers?
Data: an order for ₹1,000 was placed on 30 November, delivered on 3 December and returned on 10 December. Show how each date convention reports it.
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 Which customer data in an orders table is personal information (name, phone, address, location), and how would you share data safely with a business team?
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 In plain words, what should an e-commerce analyst know about India's Digital Personal Data Protection Act, 2023, when using customer data for analysis?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 What is order processing time or dispatch SLA in an e-commerce warehouse, and how would you measure breaches?
Data: 5,000 orders were due to be dispatched within 24 hours of payment; 4,350 were dispatched in time. Calculate the dispatch-SLA compliance and the breach count, and list cuts you would run on the breaches.
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 What is ETA accuracy in quick commerce, and how would you measure the gap between the delivery time shown to the customer and the actual time?
Data: 10 orders showed an ETA of 12 minutes; the actual times were 9, 10, 11, 12, 12, 13, 14, 15, 18 and 22 minutes. Calculate the average error, the share on time or early, and the 90th-percentile time.
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 Why can a customer order an item shown as in stock and then have it cancelled, and which data would show inventory accuracy problems?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🟡 How would you analyse refund turnaround time, and how do orders, payment-gateway and bank records get reconciled for refunds?
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🟡 How would you use hourly order data to plan pickers and riders, and how do you define a peak hour?
<!-- ANSWER_PENDING -->

### Q58 ⭐⭐ 🟡 How would you measure the time between a customer's orders in quick commerce, and what does a long gap tell you?
Data: a new customer cohort of 1,000 users; 600 placed a second order within 30 days; 300 placed a third within 60 days. Calculate the 30-day repeat rate and the second-to-third order conversion.
<!-- ANSWER_PENDING -->

### Q59 ⭐⭐ 🟡 What happens to a returned item (quality check, restock, refurbish, liquidate, destroy), and how do you measure the recovery value?
Data: 1,000 returned units worth ₹5,00,000 at selling price: 600 resold at full price, 250 resold at 50%, 150 written off. Calculate the recovery rate by value.
<!-- ANSWER_PENDING -->

### Q60 ⭐⭐ 🟡 What data and pitfalls would you consider when comparing your prices with a competitor's (pack sizes, offers, availability)?
<!-- ANSWER_PENDING -->

### Q61 ⭐⭐ 🔴 How would you decide where to open the next dark store using existing order and delivery data?
<!-- ANSWER_PENDING -->

### Q62 ⭐⭐ 🔴 A new dark store opened eight weeks ago. How would you judge whether it is ramping up well compared with older stores?
<!-- ANSWER_PENDING -->

### Q63 ⭐⭐ 🔴 Delivery times in a city rose sharply on rainy evenings. How would you separate the effect of rider supply, store capacity and distance, and what would you recommend?
<!-- ANSWER_PENDING -->

### Q64 ⭐⭐ 🔴 A membership programme (such as Prime, Flipkart VIP or Zepto Pass) claims members order more often. How would you test whether the programme caused it, given that keen buyers join more?
<!-- ANSWER_PENDING -->

### Q65 ⭐⭐ 🔴 Item fill rate dropped from 96% to 91% in 15 of 200 stores. How would you find the cause and what would you do?
<!-- ANSWER_PENDING -->

### Q66 ⭐⭐ 🔴 How do you decide which SKUs a dark store should stock, and what data would you use to rank them?
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🟢 What is a private label on an e-commerce platform, and why do platforms track its share of GMV and margin?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟡 In plain words, what do the Consumer Protection (E-Commerce) Rules and the dark-pattern guidelines mean for an analyst working on checkout, pricing and COD fees?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🟡 Does GMV include GST and delivery fees, and why does the answer matter when you compare with finance numbers?
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🟡 What does a marketplace settlement report show (orders, commission, fees, returns, payout), and how would you reconcile it with the orders table?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟡 What is a delivery slot or cut-off time (same-day, next-day, scheduled), and how would you analyse its effect on orders and cost?
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🟡 In plain words, what is the gig-worker social security provision in India, and why do analysts need to treat rider pay and location data with care?
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🟡 How would you plan seasonal workforce for a fulfilment centre ahead of a festive sale, using last year's orders and productivity data?
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🟡 Why are product ratings and reviews biased, and how would you use them in an analysis?
<!-- ANSWER_PENDING -->

### Q75 ⭐ 🟡 What dashboard or data would a brand or seller want from a marketplace, and which of it can the platform share?
<!-- ANSWER_PENDING -->

### Q76 ⭐ 🟡 What is item substitution in quick commerce, and how would you measure substitution acceptance?
<!-- ANSWER_PENDING -->

### Q77 ⭐ 🟡 What is a damaged-in-transit rate, and how would you split it between packaging, courier and handling?
<!-- ANSWER_PENDING -->

### Q78 ⭐ 🟡 Why are price experiments tricky in e-commerce, given that customers compare prices across apps?
<!-- ANSWER_PENDING -->

### Q79 ⭐ 🔴 Do faster delivery estimates raise conversion? Describe how you would analyse it and what could mislead you.
<!-- ANSWER_PENDING -->

### Q80 ⭐ 🔴 Design a seller scorecard for a marketplace: which metrics, what weights, and how would you avoid unfair penalties?
<!-- ANSWER_PENDING -->

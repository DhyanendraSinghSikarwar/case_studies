# Book 7 — Guesstimates, Case Studies & Business Metrics | Part 3: Revenue & Operations Guesstimates 🟡🔴

**Target:** 70 questions | **Actual:** 72 questions
**Scope:** revenue and operations estimation prompts (orders per day, ridership, riders and fleet sizing, capacity, order-to-revenue conversion, peak factors) plus how to structure and sanity-check them; fully specified numeric prompts carry their inputs inline.

### Q1 ⭐⭐⭐ 🟢 Estimate the number of food delivery orders a platform like Swiggy receives in India in a day.
**Asked at:** a candidate-compiled report (Board Infinity, unverified) and practice sites (Hacking the Case Interview, PrachHub) list "orders per day" for Swiggy; no company-verified paper found.
**What the interviewer is checking:** Whether you build the number from people and habits (not a memorised company figure), state assumptions and sanity-check.
**Say this in the interview:** "I will go bottom-up: people in cities the app serves, the share who order from it in a month, orders per user, then divide by 30. I get about 1.6 million orders a day, range 0.8 to 2.7 million."

**Clarify first:** One platform (Swiggy only) or the whole market? Food only or also groceries? Average day or peak? I fix: Swiggy food orders, average day, India.
**Approach:** Bottom-up (users x frequency). Top-down from 1.4 billion people wastes steps because most people are not in served cities.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| People in cities the app serves | 200 million | urban India, only larger towns covered |
| Share who order from this app in a month | 8% | online food is still a minority habit |
| Orders per such user per month | 3 | occasional user, not daily |
**Calculation:**
1. Monthly users = 200 million x 8% = 16 million.
2. Orders a month = 16 million x 3 = 48 million.
3. Orders a day = 48 million / 30 = 1.6 million.
**Result:** about 1.6 million orders a day (range 0.8 to 2.7 million).
**Sanity check:** Supply route: about 150,000 active restaurants x 10 orders a day = 1.5 million. Close to the first route.
**Sensitivity:** The share of people ordering is the shakiest input: 6% with 2 orders gives 0.8 million, 10% with 4 orders gives 2.7 million.

**Likely follow-ups:** 1) *What if it is a Sunday?* Multiply by about 1.2 to 1.3. 2) *Why divide by 30?* To turn a monthly count into a daily average.
**Common mistakes / traps:** Starting from 1.4 billion people; mixing "registered users" with "monthly ordering users"; forgetting to say average day.

### Q2 ⭐⭐⭐ 🟢 Estimate the number of passengers who ride the Delhi Metro in a day.
**Asked at:** Medium and upGrad guesstimate lists and a PM newsletter show this prompt (practice sites, unverified); no company-specific report found.
**What the interviewer is checking:** Segmenting the population, a sensible share and two trips per person, then a capacity cross-check.
**Say this in the interview:** "Catchment people x share who ride today x trips each. I land near 5 million journeys a day, about 2.5 million distinct people."

**Clarify first:** Passengers as journeys or as distinct people? Weekday average? Delhi only or NCR lines too? I fix: weekday journeys, whole network.
**Approach:** Top-down from the catchment population, then a station-capacity check from the supply side.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| People living near the network | 25 million | Delhi plus nearby NCR towns |
| Share who ride on a given day | 10% | commuters, students, shoppers |
| Journeys per rider per day | 2 | to and back |
| Stations | 250 | rough network size |
| Entries per station per day | 18,000 | mix of busy and quiet stations |
**Calculation:**
1. Riders = 25 million x 10% = 2.5 million people.
2. Journeys = 2.5 million x 2 = 5 million.
3. Supply check: 250 x 18,000 = 4.5 million entries.
**Result:** about 5 million journeys a day (range 4 to 6 million).
**Sanity check:** The two routes (5.0 and 4.5 million) are within 10%.
**Sensitivity:** The ride share drives it: 8% gives 4 million, 12% gives 6 million.

**Likely follow-ups:** 1) *Weekend?* Lower, perhaps 70 to 80% of a weekday. 2) *Peak hours?* Roughly 30 to 40% of trips fall in the two commute peaks.
**Common mistakes / traps:** Counting a return trip once; ignoring the difference between people and journeys; no cross-check.

### Q3 ⭐⭐⭐ 🟢 Estimate the number of cab rides booked on ride-hailing apps in Delhi in a day.
**Asked at:** commonly asked (no company-specific report found); ride-hailing city volumes appear on practice sites (unverified).
**What the interviewer is checking:** Choosing who is the app user, then frequency; and a supply-side check.
**Say this in the interview:** "Adults in the city, share who use cab apps in a month, rides each, divide by 30. I get about 360,000 rides a day, range 270,000 to 450,000."

**Clarify first:** Completed rides or bookings (cancellations included)? Cabs only, or autos and bikes? I fix: completed cab rides, all apps combined.
**Approach:** Bottom-up from users; check from fleet supply.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| City population | 30 million | Delhi urban area |
| Adults | 60% | rest are children and elderly |
| Adults who use cab apps monthly | 15% | not everyone owns a vehicle or uses cabs |
| Rides per user per month | 4 | occasional use |
| Active cabs a day / rides per cab | 80,000 / 5 | for the supply check |
**Calculation:**
1. Adults = 30 million x 60% = 18 million.
2. Monthly users = 18 million x 15% = 2.7 million.
3. Rides a month = 2.7 million x 4 = 10.8 million; a day = 360,000.
**Result:** about 360,000 rides a day.
**Sanity check:** Supply: 80,000 x 5 = 400,000, within 11% of the demand route.
**Sensitivity:** Share of adult users moves it most: 10% gives 240,000, 20% gives 480,000.

**Likely follow-ups:** 1) *What if you include autos?* Add a separate segment. 2) *Rides per cab seems low?* Real cabs do more; mine counts all active-in-month cabs.
**Common mistakes / traps:** Using total population; mixing bookings and completed rides; skipping the check.

### Q4 ⭐⭐⭐ 🟢 Estimate the number of e-commerce packages delivered in Hyderabad in a day.
**Asked at:** practice sites (Dataford, PrachHub) carry a "packages per city per day" prompt framed around Flipkart (unverified); no company-verified report.
**What the interviewer is checking:** Households as the unit, order frequency, and the difference between orders and packages.
**Say this in the interview:** "Households x share who shop online x orders a month, divide by 30, then add a bit for split shipments. About 120,000 packages a day."

**Clarify first:** All e-commerce or one company? Parcels only or also groceries and food? Average day or sale days? I fix: all marketplaces, parcels, normal day.
**Approach:** Bottom-up from households, cross-check from delivery staff.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 10 million | metro area |
| People per household | 4 | typical urban size |
| Households ordering online monthly | 40% | many but not all |
| Orders per such household per month | 3 | a few a month |
| Packages per order | 1.2 | split shipments |
| Delivery staff / parcels each | 1,500 / 80 | check |
**Calculation:**
1. Households = 10 million / 4 = 2.5 million.
2. Ordering households = 2.5 million x 40% = 1 million.
3. Orders a month = 3 million; a day = 100,000.
4. Packages = 100,000 x 1.2 = 120,000.
**Result:** about 120,000 packages a day (range 60,000 to 200,000).
**Sanity check:** 1,500 x 80 = 120,000.
**Sensitivity:** Share ordering and orders per month together swing it: 30% with 2 orders gives about 60,000; 50% with 4 orders gives about 200,000.

**Likely follow-ups:** 1) *Festive season?* 2 to 3 times normal. 2) *Returns?* Count separately as reverse packages.
**Common mistakes / traps:** Using people instead of households; counting orders as packages.

### Q5 ⭐⭐⭐ 🟢 Before estimating Swiggy's orders per day, which scope questions would you ask the interviewer, and why do they change the answer?
**Asked at:** practice sites (Hacking the Case Interview, PrachHub) stress scope clarification for this prompt (unverified); no company-verified report.
**What the interviewer is checking:** Whether you pin down the definition before doing arithmetic.
**Say this in the interview:** "I would ask five things: which business, which geography, which day, what counts as an order, and which year. Each can change the answer by a large factor."

**Explain simply:**
- **Business:** food only, or also grocery (Instamart-style)? Adding grocery adds a second stream.
- **Geography:** India, one city, or only served cities? This sets the population base.
- **Time:** average day, weekend, festive, or a peak hour? Weekend can be 1.2 to 1.3 times average; the peak hour is about 3 times the average hour.
- **What counts:** placed or delivered orders (cancellations)? One order or one meal (a family order has several meals)?
- **Share:** the platform alone or the whole market? A market of 3 million with a 50% share is 1.5 million.
**Mini-example:** Same inputs as Q1 give 1.6 million; if the interviewer meant "placed", add about 3% cancellations: 1.65 million. A scope miss of one factor changes the answer more than a small error in any input.
**Practice step:** Write your five scope questions on a card and say them aloud before every guesstimate.

**Likely follow-ups:** 1) *What if the interviewer says "just decide"?* State your scope in one line and proceed. 2) *Which question matters most?* Business and geography.
**Common mistakes / traps:** Skipping scope and then being corrected midway; asking ten questions and wasting time.

### Q6 ⭐⭐⭐ 🟢 How do you convert an estimate of orders per day into revenue per day for a food delivery platform? Distinguish orders, GMV, take rate and net revenue.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The four-link chain and that you never call GMV "revenue".
**Say this in the interview:** "Orders x average order value is GMV, the money customers spend. The platform keeps only a take rate of that as net revenue. I would never report GMV as income."

**Explain simply:**
- **Orders:** count of deliveries. **AOV (average order value):** average basket, in rupees. **GMV (gross merchandise value):** orders x AOV; includes the restaurant's share.
- **Take rate:** the share of GMV the platform keeps (commission, delivery fees, advertising). **Net revenue:** GMV x take rate.
- Formula in words: net revenue = orders x AOV x take rate.
**Worked example (illustrative numbers):** 100,000 orders x ₹400 = ₹4 crore GMV a day. At a 20% take rate, net revenue = ₹80 lakh a day, or ₹80 per order. Rider pay and discounts then come out of that.
**Practice step:** Re-do the example at AOV ₹500 and take rate 15%: ₹5 crore GMV, ₹75 lakh net.

**Likely follow-ups:** 1) *Why is take rate not 100%?* The restaurant and rider are paid first. 2) *Is net revenue profit?* No; costs come after.
**Common mistakes / traps:** Calling GMV revenue; applying the take rate to orders instead of GMV; mixing lakh and crore.

### Q7 ⭐⭐⭐ 🟢 A metro network carries 2.5 million riders on an average day at an average fare of ₹35. Estimate the daily and annual fare revenue.
**Given (for this question only):** 2.5 million riders/day; average fare ₹35; assume 365 operating days; ignore non-fare income.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Clean unit handling (million, crore) and multiplication.
**Say this in the interview:** "Riders x fare gives ₹8.75 crore a day, times 365 is about ₹3,194 crore a year."

**Definition in plain words:** Fare revenue = number of riders x average fare. Annual = daily x days.
**Worked answer:**
1. Daily = 2,500,000 x 35 = ₹87,500,000 = 8.75 crore (1 crore = 10 million).
2. Annual = 87,500,000 x 365 = ₹31,937,500,000 = ₹3,193.75 crore.
**Result:** ₹8.75 crore a day; about ₹3,194 crore a year.
**Check:** ₹8.75 crore x 365 = 3,193.75; rounding 8.75 to 9 gives about 3,285, so the figure is in the right range.
**Caveats:** Weekends carry fewer riders, so a flat 365 x average may overstate; "riders" should mean paid journeys; ignoring concessions and passes.

**Likely follow-ups:** 1) *What if the average fare is ₹30?* Daily 7.5 crore, annual 2,737.5 crore. 2) *Per-rider cost?* Needs cost data.
**Common mistakes / traps:** Losing zeros between million and crore; treating 2.5 million as unique people when it may be journeys.

### Q8 ⭐⭐⭐ 🟢 A delivery partner works 8 hours a day and one order takes 28 minutes from accepting to being free again. How many orders can the partner deliver in a day?
**Given:** 8 working hours; 28 minutes per order cycle; no breaks or idle time.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Units (hours to minutes) and rounding down to whole orders.
**Say this in the interview:** "480 minutes divided by 28 is 17.1, so 17 completed orders."

**Definition in plain words:** Capacity = available time / time per order, rounded down.
**Worked answer:**
1. 8 hours x 60 = 480 minutes.
2. 480 / 28 = 17.14.
3. Only whole orders count: 17 orders (17 x 28 = 476 minutes).
**Result:** 17 orders a day, about 2.1 orders an hour.
**Check:** 17 x 28 = 476 minutes, 4 minutes left, not enough for an 18th.
**Caveats:** Real days have waiting, breaks and slow hours, so true output is lower; the cycle time itself varies with distance.

**Likely follow-ups:** 1) *If cycle time falls to 24 minutes?* 480/24 = 20 orders. 2) *Why not 17.14?* You cannot deliver part of an order.
**Common mistakes / traps:** Dividing 8 by 28; rounding up to 18.

### Q9 ⭐⭐⭐ 🟢 Estimate the number of orders a quick-commerce app receives in your city in a day, and list the three assumptions that move the answer most.
**Asked at:** Blinkit-style "daily orders in a city" prompts appear in AmbitionBox and a Product Leadership guide (PM roles, unverified).
**What the interviewer is checking:** Households-based sizing, frequency, and knowing which inputs dominate.
**Say this in the interview:** "I will use Bengaluru. Households x share active x orders a month, divided by 30: about 175,000 orders a day across apps; the three big levers are active share, frequency and city size."

**Clarify first:** One app or all? Groceries only? Average day? I fix: all quick-commerce apps combined, Bengaluru, average day.
**Approach:** Bottom-up from households.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 14 million | metro area |
| People per household | 4 | typical |
| Households active monthly | 25% | affluent, dense, served areas |
| Orders per active household per month | 6 | top-up shopping |
**Calculation:**
1. Households = 14 million / 4 = 3.5 million.
2. Active = 3.5 million x 25% = 875,000.
3. Orders a month = 875,000 x 6 = 5.25 million; a day = 175,000.
**Result:** about 175,000 orders a day (range 115,000 to 280,000).
**Sanity check:** One app with a 35% share would see about 61,000 a day, close to 60 stores x 1,000 (see Q22).
**Sensitivity:** The three assumptions that move it most: (1) active share, 20% with 5 orders gives about 117,000; 30% with 8 gives 280,000; (2) frequency; (3) how much of the city is actually served.

**Likely follow-ups:** 1) *Weekday vs weekend?* Weekend higher by about 10 to 20%. 2) *Why households?* Orders are placed per home.
**Common mistakes / traps:** Counting all residents; forgetting areas not served.

### Q10 ⭐⭐⭐ 🟡 Estimate the daily revenue of one quick-commerce dark store in a metro city.
**Asked at:** Blinkit-style prompts on candidate sites (AmbitionBox, Product Leadership, unverified); no company-verified report.
**What the interviewer is checking:** Splitting orders, AOV and take rate, and saying whether "revenue" means GMV or net.
**Say this in the interview:** "1,000 orders x ₹500 is ₹5 lakh GMV; at an 18% take rate the store earns about ₹90,000 a day in net revenue."

**Clarify first:** Revenue as GMV or what the company keeps? Average day? I fix: both, average day.
**Approach:** Bottom-up from the store's orders.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Orders a day | 1,000 | busy metro store |
| Average order value | ₹500 | mix of staples and snacks |
| Take rate (margin plus fees) | 18% | assumed |
**Calculation:**
1. GMV = 1,000 x 500 = ₹5,00,000 (₹5 lakh).
2. Net revenue = 5,00,000 x 18% = ₹90,000.
**Result:** GMV about ₹5 lakh a day; net revenue about ₹90,000.
**Sanity check:** Orders per hour over 16 open hours = 62, about 1 a minute: plausible for a busy store.
**Sensitivity:** Orders matter most: 800 to 1,200 orders and AOV ₹400 to ₹600 give ₹3.2 lakh to ₹7.2 lakh GMV.

**Likely follow-ups:** 1) *Is it profitable?* Needs rent, pay and rider costs. 2) *How to grow it?* Raise AOV or orders per area.
**Common mistakes / traps:** Reporting GMV as revenue; using city-level orders.

### Q11 ⭐⭐⭐ 🟡 Estimate the number of orders an e-commerce platform like Flipkart receives on the first day of its annual festive sale.
**Asked at:** practice sites (Dataford, PrachHub) list sale-day orders as a Flipkart-style prompt (unverified); a news item on orders per second inspired Q16 only.
**What the interviewer is checking:** Active buyers, sale-day uplift, and a rate-per-second sanity check.
**Say this in the interview:** "Monthly buyers x share who buy on day one x orders each: about 3 million orders on day one, range 2 to 5 million."

**Clarify first:** First 24 hours or sale-day business hours? Orders or items? I fix: orders in 24 hours.
**Approach:** Users x conversion, checked by per-second rate.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Monthly active buyers in festive period | 80 million | large platform |
| Share buying on day one | 3% | early-access and deal hunters |
| Orders per buyer that day | 1.3 | a few buy twice |
**Calculation:**
1. Day-one buyers = 80 million x 3% = 2.4 million.
2. Orders = 2.4 million x 1.3 = 3.12 million.
3. Rate = 3.12 million / 86,400 s = 36 orders per second on average; a 3x peak is about 108 per second.
**Result:** about 3 million orders (range 2 to 5 million).
**Sanity check:** A 108-per-second peak is the same order as rates seen in sale news (see Q16), so the scale holds.
**Sensitivity:** Day-one share: 2% gives about 2.1 million, 5% gives about 5.2 million.

**Likely follow-ups:** 1) *Normal day?* Perhaps one fifth. 2) *Value in rupees?* Orders x AOV for GMV.
**Common mistakes / traps:** Using all registered users; forgetting uplift versus normal days.

### Q12 ⭐⭐⭐ 🟡 Estimate the number of delivery riders a food delivery app needs in Bengaluru during the dinner peak.
**Asked at:** practice site PrachHub lists a Zomato rider-fleet-in-Bengaluru prompt (unverified); no company-verified report.
**What the interviewer is checking:** Peak-hour factor and rider productivity, then roster versus on-road riders.
**Say this in the interview:** "Daily orders, a dinner share, orders per rider per hour: about 15,000 riders on the road at peak, around 19,000 on the roster."

**Clarify first:** One app or all? Riders on the road or total roster? I fix: one app, riders on the road at peak, then a roster uplift.
**Approach:** Demand in the peak hour divided by one rider's hourly output.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| App orders a day in Bengaluru | 250,000 | about 45 to 50% of all food orders (see Q19) |
| Share in 3-hour dinner peak | 35% | 7 to 10 pm |
| Orders per rider per hour | 2 | cycle of about 28 minutes |
| Roster uplift | 30% | breaks, absentees |
**Calculation:**
1. Peak orders = 250,000 x 35% = 87,500.
2. Per hour = 87,500 / 3 = 29,167.
3. Riders on road = 29,167 / 2 = 14,583.
4. Roster = 14,583 x 1.3 = 18,958, about 19,000.
**Result:** about 15,000 riders on the road (range 12,000 to 19,000).
**Sanity check:** 14,583 riders x 2 orders x 3 hours = 87,500, matching peak orders.
**Sensitivity:** Rider productivity: 2.5 orders an hour gives about 11,700; 1.5 gives about 19,400.

**Likely follow-ups:** 1) *Rain?* Cycle time up, so more riders. 2) *Lunch peak?* Smaller, perhaps 25%.
**Common mistakes / traps:** Dividing daily orders by orders per rider per day, ignoring peak.

### Q13 ⭐⭐⭐ 🟡 A dark store handles 1,000 orders a day and 40% of them arrive in a 4-hour evening peak. One rider completes 2.5 orders per hour. How many riders are needed during the peak?
**Given:** 1,000 orders/day; 40% in a 4-hour peak; 2.5 orders per rider per hour; no buffer for absenteeism.
**Asked at:** AmbitionBox and a Product Leadership guide mention riders-per-store from orders per hour (PM roles, unverified).
**What the interviewer is checking:** Converting a daily total into an hourly peak, then dividing by productivity.
**Say this in the interview:** "400 peak orders over 4 hours is 100 an hour; at 2.5 per rider that is 40 riders."

**Definition in plain words:** Riders needed = peak orders per hour / orders per rider per hour.
**Worked answer:**
1. Peak orders = 1,000 x 40% = 400.
2. Per hour = 400 / 4 = 100.
3. Riders = 100 / 2.5 = 40.
**Result:** 40 riders during the peak.
**Check:** 40 x 2.5 x 4 = 400 orders.
**Caveats:** Orders are not spread evenly inside the peak; add a buffer (about 10 to 15%) for absentees, which would give 44 to 46; the daily average is only 62 orders an hour over 16 hours.

**Likely follow-ups:** 1) *With 10% buffer?* 44 riders. 2) *Off-peak?* 600 / 12 hours = 50 an hour, so 20 riders.
**Common mistakes / traps:** Using 1,000 orders for the peak; dividing by 4 twice.

### Q14 ⭐⭐⭐ 🟡 Estimate the number of meals a food delivery app delivers in Mumbai on an average day.
**Asked at:** a ProductFolks practice page lists a Swiggy Mumbai meals prompt (unverified); no company-verified report.
**What the interviewer is checking:** The order-to-meal conversion, not just orders.
**Say this in the interview:** "Households ordering x orders a month gives about 175,000 orders a day; at 1.5 meals an order that is about 260,000 meals."

**Clarify first:** One app or all? A "meal" as one person's dish? I fix: one app, meals = plates served.
**Approach:** Bottom-up from households, then a meals-per-order multiplier.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 21 million | metro region |
| People per household | 4 | typical |
| Households ordering from this app monthly | 20% | dense city |
| Orders per household per month | 5 | |
| Meals per order | 1.5 | some orders are for two |
**Calculation:**
1. Households = 21 million / 4 = 5.25 million.
2. Ordering = 5.25 million x 20% = 1.05 million.
3. Orders a month = 5.25 million; a day = 175,000.
4. Meals = 175,000 x 1.5 = 262,500.
**Result:** about 260,000 meals a day (range 160,000 to 390,000).
**Sanity check:** Population route: 21 million x 1.2% eat an app meal a day = about 250,000.
**Sensitivity:** Ordering share: 15% with 4 orders gives about 158,000; 25% with 6 gives about 394,000.

**Likely follow-ups:** 1) *Weekend?* 20 to 30% higher. 2) *Why meals not orders?* Meals reflect group orders.
**Common mistakes / traps:** Treating orders and meals as equal; using the wrong population for "Mumbai".

### Q15 ⭐⭐⭐ 🟡 You estimated 2 million Swiggy orders a day for India. Give three independent cross-checks you would use to sanity-check that number.
**Asked at:** commonly asked (no company-specific report found); a public benchmark exists but no figure is used here.
**What the interviewer is checking:** Triangulation: checks from different angles, not repeats.
**Say this in the interview:** "Check from users, from restaurants and from riders; each uses different inputs and all should land near 2 million."

**Explain simply:**
- **Users:** 20 million monthly users x 3 orders / 30 = 2.0 million.
- **Restaurants:** about 150,000 active partners x 13 orders a day = 1.95 million.
- **Riders:** about 300,000 riders x 7 orders a day = 2.1 million.
- **Money and rate:** 2 million x ₹400 = ₹80 crore GMV a day (₹29,200 crore a year); and 2 million / 86,400 s = 23 orders a second. If the annual figure looks far from public annual reports (look them up), revisit assumptions.
- All inputs are assumed, approximate, unverified.
**Mini-example:** If the user check gave 2.0 million but the rider check gave 0.5 million, ask whether riders work for several apps.
**Practice step:** For any estimate, write down one user, one supply and one money check.

**Likely follow-ups:** 1) *Which check is strongest?* The one with the best-known input. 2) *What if they disagree?* Find the weak assumption.
**Common mistakes / traps:** Repeating the same inputs; treating a check as proof.

### Q16 ⭐⭐⭐ 🟡 A sale-day platform logs 110 orders per second during a 1-hour peak and an average of 20 orders per second over the remaining 23 hours. How many orders does it receive that day?
**Given:** 110 orders/s for 3,600 s; 20 orders/s for the other 82,800 s.
**Asked at:** a news report on orders per second inspired the figure; used only as an exercise input.
**What the interviewer is checking:** Rate x time with split periods.
**Say this in the interview:** "Peak 396,000 plus off-peak 1,656,000 gives about 2.05 million orders."

**Definition in plain words:** Orders = rate per second x seconds, summed over periods.
**Worked answer:**
1. Peak = 110 x 3,600 = 396,000.
2. Rest = 20 x 82,800 = 1,656,000.
3. Total = 2,052,000.
**Result:** about 2.05 million orders a day.
**Check:** Average rate = 2,052,000 / 86,400 = 23.75 orders a second; that is close to the off-peak rate because the peak is only 1 hour.
**Caveats:** The peak hour contributes 19% of orders; a single average rate misses this shape.

**Likely follow-ups:** 1) *Peak to average ratio?* 110 / 23.75 = 4.6. 2) *Servers?* Size for the peak.
**Common mistakes / traps:** Using 24 hours for the off-peak; forgetting 3,600 seconds per hour.

### Q17 ⭐⭐⭐ 🟡 A food delivery platform gets 1.5 million orders a day at an average order value of ₹400 and earns 25% of GMV as net revenue. What is its annual net revenue in ₹ crore?
**Given:** 1.5 million orders/day; AOV ₹400; net revenue = 25% of GMV; 365 days; 1 crore = 10 million.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The chain orders to GMV to net revenue, and unit care.
**Say this in the interview:** "GMV is ₹60 crore a day, net revenue ₹15 crore a day, about ₹5,475 crore a year."

**Definition in plain words:** Net revenue = orders x AOV x take rate; annual = daily x 365.
**Worked answer:**
1. Daily GMV = 1,500,000 x 400 = ₹600,000,000 = ₹60 crore.
2. Daily net revenue = 60 crore x 25% = ₹15 crore.
3. Annual = 15 x 365 = ₹5,475 crore.
**Result:** ₹5,475 crore a year.
**Check:** Annual GMV = ₹21,900 crore; 25% of that = 5,475.
**Caveats:** A 25% share of GMV is high for such platforms (I treat it only as the exercise input); real take rates are usually lower and fall after discounts and delivery costs.

**Likely follow-ups:** 1) *At 20%?* 4,380 crore. 2) *Why use 365?* Platforms run every day.
**Common mistakes / traps:** Mistaking 600 million for 600 crore; applying 25% to orders.

### Q18 ⭐⭐⭐ 🟡 Estimate the revenue a cab aggregator earns from airport trips at one city airport in a day.
**Asked at:** one Glassdoor candidate report (a business analyst interview, 2026 per search summary, unverified) mentions an Uber revenue from Delhi airport guesstimate.
**What the interviewer is checking:** Passenger funnel, then fare, and separating trip value from the company's commission.
**Say this in the interview:** "Airport passengers x share using app cabs / party size x fare gives about ₹1.6 crore trip value; the aggregator keeps about ₹33 lakh at 20%."

**Clarify first:** Pickups and drop-offs both? Revenue as trip value or commission? I fix: both directions, report trip value and company revenue.
**Approach:** Funnel from passengers.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Airport passengers a day (arrivals plus departures) | 150,000 | large metro airport |
| Share using app cabs | 25% | others use own car, taxi, metro |
| Passengers per ride | 1.6 | solo and families |
| Average fare | ₹700 | airport trips are long |
| Aggregator commission | 20% | assumed |
**Calculation:**
1. App-cab passengers = 150,000 x 25% = 37,500.
2. Rides = 37,500 / 1.6 = 23,438.
3. Trip value = 23,438 x 700 = ₹1.64 crore.
4. Aggregator revenue = 20% x 1.64 crore = ₹32.8 lakh.
**Result:** about 23,000 rides, ₹1.6 crore trip value, ₹33 lakh company revenue a day.
**Sanity check:** 23,000 rides over 24 hours is about 1,000 an hour; plausible for a major airport.
**Sensitivity:** App share: 15% with fare ₹600 and 15% commission gives about ₹13 lakh; 30% with fare ₹800 and 25% gives about ₹56 lakh.

**Likely follow-ups:** 1) *Surge or night?* Raise fare assumption. 2) *Share between apps?* Multiply by market share.
**Common mistakes / traps:** Counting passengers as rides; reporting trip value as company revenue.

### Q19 ⭐⭐⭐ 🟡 Estimate the number of online food delivery orders placed in Bengaluru on a typical Sunday.
**Asked at:** a Dataford practice page lists this as a PhonePe-framed prompt (unverified); no company-verified report.
**What the interviewer is checking:** Average first, then a day-of-week factor.
**Say this in the interview:** "Average day about 417,000 orders across apps; Sunday runs about 1.3 times higher, so roughly 540,000."

**Clarify first:** All apps? Only food (no grocery)? Placed or delivered? I fix: all apps, food, placed.
**Approach:** Bottom-up users x frequency, then weekend factor.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Active online food users in the city | 2.5 million | about 18% of 14 million people |
| Orders per user per month | 5 | |
| Sunday factor | 1.3 | weekend demand |
**Calculation:**
1. Orders a month = 2.5 million x 5 = 12.5 million.
2. Average day = 12.5 million / 30 = 416,667.
3. Sunday = 416,667 x 1.3 = 541,667.
**Result:** about 540,000 orders (range 300,000 to 820,000).
**Sanity check:** 540,000 / 14 million people is 0.04 orders per person, one order for every 26 people, plausible for a food-app city.
**Sensitivity:** Users and frequency: 2.5 million with 3 orders at 1.2 gives 300,000; with 7 orders at 1.4 gives about 817,000.

**Likely follow-ups:** 1) *Sunday dinner peak?* About one third of the day in 3 hours. 2) *Monsoon?* Higher.
**Common mistakes / traps:** Using average day for Sunday; mixing users with households.

### Q20 ⭐⭐⭐ 🟡 Estimate the number of UPI payment transactions made in India in a day.
**Asked at:** commonly asked (no company-specific report found); a UPI revenue prompt could not be sourced.
**What the interviewer is checking:** Active users x frequency, and the reality check against population.
**Say this in the interview:** "Active UPI users times transactions a month, divide by 30: about 400 million a day, range 270 to 600 million."

**Clarify first:** Count all UPI payments (person-to-person and merchant)? Successful ones only? I fix: all successful transactions, average day.
**Approach:** Bottom-up from active users.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Monthly active UPI users | 400 million | smartphone adults |
| Transactions per user a month | 30 | about one a day |
**Calculation:**
1. Monthly = 400 million x 30 = 12 billion.
2. Daily = 12 billion / 30 = 400 million.
**Result:** about 400 million a day (range 270 to 600 million).
**Sanity check:** Spread over 1.4 billion people it is 0.29 a day each, about 1 transaction per 3.5 people daily; looks plausible. The figure should be checked against published figures (not verified here).
**Sensitivity:** Per-user frequency: 20 a month gives 267 million; 45 gives 600 million.

**Likely follow-ups:** 1) *Value?* Transactions x average ticket (small). 2) *Peak?* Evenings and month start.
**Common mistakes / traps:** Counting registered accounts; forgetting the divide by 30.

### Q21 ⭐⭐⭐ 🟡 A food delivery app has 20 million monthly transacting users who order on average 3 times a month. How many orders per day is that, and what does it imply for the daily order estimate?
**Given:** 20 million monthly transacting users; 3 orders per user per month; 30-day month.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Monthly to daily conversion and honest use of an average.
**Say this in the interview:** "60 million orders a month is 2 million a day, which supports a 2 million daily estimate."

**Definition in plain words:** Daily orders = monthly users x orders per user / days in month.
**Worked answer:**
1. Monthly orders = 20,000,000 x 3 = 60,000,000.
2. Daily = 60,000,000 / 30 = 2,000,000.
**Result:** 2 million orders a day (about 730 million a year).
**Check:** 2,000,000 x 30 = 60,000,000.
**Caveats:** It matches the 2 million estimate in Q15, but it is an average day: weekends and peaks are higher; the 3 is an average, so heavy users matter; "monthly transacting" must exclude inactive installs.

**Likely follow-ups:** 1) *If users order 2.5 times?* 1.67 million. 2) *Weekend?* About 1.3 times.
**Common mistakes / traps:** Dividing by 365 instead of 30.

### Q22 ⭐⭐⭐ 🔴 Estimate how many dark stores a quick-commerce company needs to cover a large metro city such as Bengaluru.
**Asked at:** Blinkit-style questions appear on candidate sites (AmbitionBox, Product Leadership, PM roles, unverified); no company-verified report.
**What the interviewer is checking:** Two views, coverage by area and capacity by demand, and picking the binding one.
**Say this in the interview:** "Area says about 64 stores; demand says about 61. I would plan about 60 to 65 stores."

**Clarify first:** One company? Only the served core? Target delivery time (say 10 to 15 minutes)? I fix: one company with a 35% market share, served city area, a 2 km radius.
**Approach:** Both routes; the higher number binds.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Served urban area | 600 km2 | not the whole city limit |
| Delivery radius | 2 km | for fast delivery |
| Usable coverage | 75% | circles overlap and have gaps |
| City quick-commerce orders a day | 175,000 | from Q9 |
| Company share | 35% | |
| Orders per store a day | 1,000 | busy store |
**Calculation:**
1. Area per store = 3.14 x 2 x 2 x 75% = 9.4 km2.
2. Area route = 600 / 9.4 = 64 stores.
3. Company orders = 175,000 x 35% = 61,250.
4. Demand route = 61,250 / 1,000 = 61 stores.
**Result:** about 60 to 65 stores.
**Sanity check:** 61 stores x 1,000 orders = 61,000, in line with the share estimate.
**Sensitivity:** Radius matters most: at 2.5 km the area route drops to about 41 stores.

**Likely follow-ups:** 1) *Which binds?* Area in suburbs, demand in dense areas. 2) *Cost?* Needs store economics.
**Common mistakes / traps:** Using only one route; using the whole city limit.

### Q23 ⭐⭐⭐ 🔴 Estimate the number of food delivery orders nationwide at 8 pm on a Saturday, and explain how you adjust from the daily average to a peak hour.
**Asked at:** a PrachHub practice page lists a nationwide hourly-throughput Swiggy prompt (unverified); no company-verified report.
**What the interviewer is checking:** Average day, then a weekday factor, then an hourly share.
**Say this in the interview:** "Average 2 million a day, Saturday 1.2 times, the 8 pm hour carries 12% of the day: about 288,000 orders, roughly 80 a second."

**Clarify first:** One platform or all? The 8 to 9 pm hour? I fix: one platform (Q15's 2 million), the 8 to 9 pm hour.
**Approach:** Daily average, then day factor, then hour share; compare with a flat hour.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Average daily orders | 2 million | from Q15 |
| Saturday factor | 1.2 | weekend uplift |
| Share of day in the 8 to 9 pm hour | 12% | dinner peak |
**Calculation:**
1. Saturday orders = 2 million x 1.2 = 2.4 million.
2. 8 pm hour = 2.4 million x 12% = 288,000.
3. Per second = 288,000 / 3,600 = 80.
4. Peak factor = 12% / (1/24 = 4.17%) = 2.9 times the average hour.
**Result:** about 290,000 orders in that hour (range 240,000 to 340,000).
**Sanity check:** An even spread would be 100,000 an hour; 2.9 times is a reasonable peak.
**Sensitivity:** Hour share: 10% gives 240,000; 14% gives 336,000.

**Likely follow-ups:** 1) *Why not 1/24?* Orders cluster at meals. 2) *What about IPL or rain?* Further uplift.
**Common mistakes / traps:** Using the daily average for the hour; confusing share of the day with a rate.

### Q24 ⭐⭐ 🟢 A cab driver completes 12 trips a day at an average fare of ₹180. The platform keeps 20% commission and fuel costs ₹800 a day. What is the driver's net daily earning?
**Given:** 12 trips; fare ₹180; 20% commission on fare; fuel ₹800; ignore other costs.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Ordered deductions on a simple unit economics sum.
**Say this in the interview:** "Gross fares ₹2,160, commission ₹432, fuel ₹800: ₹928 net a day."

**Definition in plain words:** Net earning = fares - commission - fuel.
**Worked answer:**
1. Gross fares = 12 x 180 = ₹2,160.
2. Commission = 20% x 2,160 = ₹432.
3. After commission = 2,160 - 432 = ₹1,728.
4. Net = 1,728 - 800 = ₹928.
**Result:** ₹928 per day (about ₹24,000 a month at 26 working days).
**Check:** 80% of 2,160 = 1,728, minus 800 = 928.
**Caveats:** It ignores vehicle loan, maintenance, insurance and idle time, so true take-home is lower; fuel is 37% of gross fares here.

**Likely follow-ups:** 1) *If commission is 25%?* 2,160 x 0.75 - 800 = ₹820. 2) *Break-even trips?* 800 / (180 x 0.8) = 5.6, so 6 trips cover fuel.
**Common mistakes / traps:** Subtracting commission from net after fuel; applying 20% to the wrong base.

### Q25 ⭐⭐ 🟢 A payroll team pays delivery partners ₹40 per order plus incentives equal to 10% of base payout. If 1.2 million orders are delivered in a day, what is the daily payout in ₹ crore?
**Given:** 1.2 million orders; ₹40/order; incentive = 10% of base payout; 1 crore = 10 million.
**Asked at:** commonly asked (no company-specific report found); gap-fill payroll-style calculation.
**What the interviewer is checking:** Clean unit conversion (million to crore) and applying the incentive on the base, not on the orders.
**Say this in the interview:** "Base payout is orders times rate, incentive is 10% on top, so total is 1.1 times base: about ₹5.28 crore a day."
**Definition in plain words:** Total payout = base payout + incentive, where base = orders x rate per order and incentive = 10% x base.
**Worked answer:**
1. Base = 1,200,000 x ₹40 = ₹48,000,000 = ₹4.8 crore (1 crore = 10,000,000).
2. Incentive = 10% x 4.8 = ₹0.48 crore.
3. Total = 4.8 + 0.48 = ₹5.28 crore.
**Result:** ₹5.28 crore per day (about ₹5.3 crore); effective ₹44 per order.
**Check:** 1.1 x 40 = ₹44; 1.2 million x 44 = 52.8 million = 5.28 crore. Matches.
**Caveats:** Real incentives are often per-slab or per-rider, not a flat 10%; the question treats it as flat. Payroll would also add statutory or insurance costs, ignored here.
**Likely follow-ups:** 1) *Monthly cost?* 5.28 x 30 = ₹158.4 crore. 2) *Per rider if 60,000 riders?* 52.8 million / 60,000 = ₹880 a day.
**Common mistakes / traps:** Mixing lakh, million and crore (1.2 million is 12 lakh); applying 10% to the order count; forgetting that crore = 10 million.

### Q26 ⭐⭐ 🟢 An edtech app has 40,000 paying learners at ₹600 per month. What is its monthly recurring revenue and annualised run-rate in ₹ crore?
**Given:** 40,000 learners; ₹600/month each; 1 crore = 10 million; no churn or discounts.
**Asked at:** commonly asked (no company-specific report found); gap-fill SaaS-style calculation.
**What the interviewer is checking:** Whether you know MRR (monthly recurring revenue) and that run-rate means current month times 12.
**Say this in the interview:** "MRR is learners times price: ₹2.4 crore a month, so the annual run-rate is ₹28.8 crore."
**Definition in plain words:** MRR = money the subscriptions bring in every month = paying users x price per month. Annualised run-rate (ARR) = MRR x 12, "what a year would be if today's month simply repeated".
**Worked answer:**
1. MRR = 40,000 x 600 = ₹24,000,000 = ₹2.4 crore.
2. Run-rate = 2.4 x 12 = ₹28.8 crore.
**Result:** MRR ₹2.4 crore; annualised run-rate ₹28.8 crore.
**Check:** 40,000 x 7,200 (annual price) = 288,000,000 = 28.8 crore.
**Caveats:** Run-rate is not forecast revenue: churn (learners leaving), discounts, GST and refunds would lower it, and growth would raise it. Annual plans paid upfront blur "monthly" recurring revenue.
**Likely follow-ups:** 1) *If 5% churn a month with no new learners?* Month 2 MRR = 2.28 crore. 2) *Is it profit?* No, revenue only.
**Common mistakes / traps:** Multiplying by 12 and calling it "this year's revenue"; slipping a zero between lakh and crore.

### Q27 ⭐⭐ 🟢 What is the difference between a top-down and a bottom-up estimate for an operations question such as the size of a rider fleet? Which would you use first?
**Asked at:** commonly asked (no company-specific report found); a Zomato rider fleet in Bengaluru prompt appears on a practice site (unverified).
**What the interviewer is checking:** That you know both methods and use one to check the other.
**Say this in the interview:** "I would start bottom-up from orders and rider productivity because it shows my logic, then cross-check top-down from population."
**Explain simply:**
- Top-down: start from a big total (city population, total orders) and slice it down with shares. Quick, but depends on a few big ratios.
- Bottom-up: build from the smallest unit (one rider's orders per hour) and scale up. Slower, but each step is checkable.
- Mini example (all assumed, unverified): a city has 12 million people. Top-down: 1 active rider per 1,000 people = 12,000 riders. Bottom-up: 60,000 orders a day, 12% in the busiest hour = 7,200 orders/hour, 2.5 orders per rider per hour = 2,880 riders at peak, x 1.4 for weekly offs and absences = about 4,000 on the roster.
- The gap (12,000 vs 4,000) is useful: it suggests riders work part time or on several apps, so I would find which input is wrong.
- Use first: bottom-up when the interviewer gives operational detail (orders, speed); top-down when you know the market total. Always do both.
- Practice step: repeat for "agents in a call centre" with both routes.
**Likely follow-ups:** 1) *Which is more accurate?* Neither alone; agreement between them builds confidence. 2) *What if they disagree by 3x?* Hunt the biggest assumption.
**Common mistakes / traps:** Presenting only one route; not reconciling a 3x gap; hiding assumptions.

### Q28 ⭐⭐ 🟢 Estimate the daily revenue of a busy multiplex in a tier-1 city.
**Asked at:** commonly asked (no company-specific report found); gap-fill revenue-per-venue prompt.
**What the interviewer is checking:** Capacity x utilisation x price, with food and beverage (F&B) as a second revenue stream.
**Say this in the interview:** "Bottom-up from seats and shows: about 3,200 tickets a day, roughly ₹13 lakh a day including snacks."
**Clarify first:** A 8-screen multiplex, an average day (weekday and weekend blended), ticket plus F&B revenue, no ad or parking income.
**Approach:** Bottom-up from seats, because the venue has a physical capacity that caps the answer.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Screens | 8 | busy tier-1 multiplex |
| Seats per screen | 250 | typical mix of large and small halls |
| Shows per day | 4 | morning to late night |
| Average occupancy | 40% | weekdays low, weekends high |
| Average ticket | ₹300 | mix of cheap and premium seats |
| F&B per viewer | ₹120 | popcorn and drink, not all buy |
**Calculation:**
1. Seats per day = 8 x 250 x 4 = 8,000.
2. Tickets = 8,000 x 40% = 3,200.
3. Ticket revenue = 3,200 x 300 = ₹9.6 lakh.
4. F&B = 3,200 x 120 = ₹3.84 lakh.
5. Total = ₹13.44 lakh.
**Result:** about ₹13 lakh a day (range ₹10 to 20 lakh).
**Sanity check:** ₹13.4 lakh x 365 = about ₹49 crore a year for one site, a plausible scale for a busy multiplex (unverified).
**Sensitivity:** Occupancy matters most: 30% gives ₹9.6 lakh, 50% (at ₹350 ticket, ₹140 F&B) gives ₹19.6 lakh.
**Likely follow-ups:** 1) *Weekend vs weekday?* Raise occupancy to 70% and price; weekend can be double. 2) *Other revenue?* Ads, parking, ticket convenience fees.
**Common mistakes / traps:** Assuming 100% occupancy; forgetting the F&B stream; ignoring that a film release drives huge swings.

### Q29 ⭐⭐ 🟢 Why is a peak-hour factor important when you estimate riders, agents or dark-store capacity from a daily order number?
**Asked at:** commonly asked (no company-specific report found); a nationwide hourly throughput prompt appears on a practice site (unverified).
**What the interviewer is checking:** You know that capacity is sized for the busiest hour, not the daily average.
**Say this in the interview:** "Demand is uneven through the day, so a team sized on the average will fail at lunch and dinner. I size for the peak hour."
**Explain simply:**
- Peak-hour factor = orders in the busiest hour divided by the average hour (or the share of the day's orders in that hour).
- Worked example (assumed numbers): 1.2 million orders a day, app active 14 hours. Average hour = 85,714 orders. If the peak hour holds 12% of the day = 144,000 orders, the factor is 1.68.
- With 2.5 orders per rider per hour: average sizing = 34,286 riders; peak sizing = 57,600 riders. The average-based plan is about 40% short at the peak.
- Not sizing for peak means late deliveries, cancellations and lost orders; sizing for peak always means idle riders off-peak, so companies use shifts, incentives and surge pricing to flatten the curve.
- Practice step: pull hourly order counts, divide the busiest hour by the daily average hour.
**Likely follow-ups:** 1) *Do you size for the single busiest hour?* Usually a high percentile such as 90th, to avoid costly overstaffing. 2) *Does it differ by day?* Yes: weekends and events.
**Common mistakes / traps:** Dividing the daily number by 24 when the app only runs 14 hours; using the average and promising an SLA (service level) at peak.

### Q30 ⭐⭐ 🟢 An app has 2 million orders a day and 3% are cancelled after the rider is assigned, costing ₹20 each in wasted payout. What is the monthly cost of these cancellations in ₹ crore?
**Given:** 2 million orders/day; 3% cancelled after assignment; ₹20 wasted per cancellation; 30-day month; 1 crore = 10 million.
**Asked at:** commonly asked (no company-specific report found); gap-fill cost-of-cancellation calculation.
**What the interviewer is checking:** Chaining a rate, a unit cost and a time scale without a unit slip.
**Say this in the interview:** "60,000 cancellations a day at ₹20 is ₹12 lakh a day, so ₹3.6 crore a month."
**Definition in plain words:** Cancellation cost = orders x cancel rate x wasted payout per cancellation, scaled to the month.
**Worked answer:**
1. Cancellations per day = 2,000,000 x 3% = 60,000.
2. Daily waste = 60,000 x ₹20 = ₹1,200,000 = ₹12 lakh.
3. Monthly = 1.2 million x 30 = ₹36 million = ₹3.6 crore.
**Result:** ₹3.6 crore a month (about ₹43 crore a year).
**Check:** 2 million x 30 = 60 million orders; 3% = 1.8 million; x 20 = 36 million. Same.
**Caveats:** Real cost also includes lost margin, refunds and customer trust; the 3% is the exercise input. Cancellation after assignment is the costly kind; before assignment costs nearly nothing.
**Likely follow-ups:** 1) *Value of cutting to 2%?* Saves ₹1.2 crore a month. 2) *Which cancellations are controllable?* Restaurant delays and no-shows, found by reason code.
**Common mistakes / traps:** Using 30 days of 3% of only one day; counting 3% of orders already cancelled before assignment.

### Q31 ⭐⭐ 🟡 Estimate the number of tickets sold on an online railway booking platform in a day.
**Asked at:** commonly asked (no company-specific report found); gap-fill, similar to a Delhi Metro riders method seen on practice blogs (unverified).
**What the interviewer is checking:** Population-to-trips decomposition with a distinction between passengers and tickets.
**Say this in the interview:** "Top-down from population: about 1.15 million reserved journeys a day, roughly 4.6 lakh online tickets, since one ticket covers about two people."
**Clarify first:** Reserved long-distance tickets only (not suburban or platform tickets), one-way journeys, one national platform, count tickets (PNR bookings), not passengers.
**Approach:** Top-down from population; a bottom-up from train seats is the cross-check.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 1.4 billion | round figure |
| Share who take reserved train trips in a year | 15% | the rest never or rarely |
| One-way reserved journeys per such person | 2 per year | one return trip |
| Share booked online | 80% | most reserved booking is online |
| Passengers per ticket | 2 | families and groups |
**Calculation:**
1. Travellers = 1.4 billion x 15% = 210 million.
2. Journeys per year = 210 million x 2 = 420 million; per day = 420 million / 365 = 1.15 million.
3. Online passengers = 1.15 million x 80% = 0.92 million.
4. Tickets = 0.92 million / 2 = 0.46 million.
**Result:** about 4.6 lakh tickets a day (range 2.7 to 6.9 lakh).
**Sanity check:** Bottom-up: if about 3,000 long-distance trains run with about 1,000 reserved seats each, one-way seats per day are about 3 million; at 75% fill and 40% of trips booked online, that is roughly 0.9 million passengers, consistent with step 3 (inputs unverified).
**Sensitivity:** The 15% traveller share moves the answer proportionally: 10% gives 2.7 lakh, 20% gives 6.9 lakh.
**Likely follow-ups:** 1) *Festival days?* Booking opens 60+ days ahead so dates spike. 2) *Why tickets not passengers?* Platform volume is counted in bookings.
**Common mistakes / traps:** Mixing journeys and tickets; counting unreserved and suburban trips; treating booking day as travel day (they differ).

### Q32 ⭐⭐ 🟡 A warehouse needs 250 pickers on duty every day. Each picker has one weekly off (6 working days a week) and absenteeism on working days is 8%. How many pickers should be on the roster?
**Given:** 250 needed on duty daily; 6 of 7 days worked; 8% absenteeism on scheduled days. Round up to a whole person.
**Asked at:** commonly asked (no company-specific report found); gap-fill workforce-planning calculation (fits an HR candidate well).
**What the interviewer is checking:** Applying both the weekly-off factor and the absenteeism factor in the right direction.
**Say this in the interview:** "I gross up for absence first, then for weekly offs: 250 / 0.92 x 7/6 = 317.03, so 318 pickers."
**Definition in plain words:** Roster size = people needed on duty / (share who actually turn up) x (days in week / days worked per person).
**Worked answer:**
1. Present rate = 1 - 8% = 0.92. To have 250 present, schedule 250 / 0.92 = 271.74 per day.
2. Each person works 6 of 7 days, so one day's schedule needs 7/6 people per slot: 271.74 x 7/6 = 317.03.
3. Round up: 318.
**Result:** 318 pickers on the roster.
**Check:** 318 x 6/7 = 272.6 scheduled per day; x 0.92 = 250.8 present, at least 250. With 317: 271.7 x 0.92 = 249.9, just short, so round up is right.
**Caveats:** Absenteeism is not evenly spread (Mondays, post-festival are worse); leave and attrition would add more; ignoring both is a trap.
**Likely follow-ups:** 1) *If shrinkage rose to 12%?* 250 / 0.88 x 7/6 = 331.4, so 332. 2) *Cost of extra headcount?* Roster x daily wage; weigh against overtime.
**Common mistakes / traps:** Multiplying by 1.08 instead of dividing by 0.92; applying only one factor; forgetting to round up.

### Q33 ⭐⭐ 🟡 A customer support centre receives 1,200 calls in its busiest hour; average handling time is 6 minutes, target occupancy is 80% and shrinkage (breaks, leave, training) is 30%. How many agents must be rostered for that hour?
**Given:** 1,200 calls/hour; 6 min AHT; 80% occupancy; 30% shrinkage. Round up. Ignore Erlang-style queue refinements.
**Asked at:** commonly asked (no company-specific report found); gap-fill workforce-management calculation.
**What the interviewer is checking:** Workload in hours, then occupancy, then shrinkage, in that order.
**Say this in the interview:** "Workload is 120 agent-hours; at 80% occupancy I need 150 on calls; with 30% shrinkage I roster 215."
**Definition in plain words:** AHT (average handling time) is talk plus after-call work per call. Occupancy is the share of logged-in time spent handling calls. Shrinkage is the share of paid time agents are unavailable.
**Worked answer:**
1. Workload = 1,200 calls x 6 min = 7,200 minutes = 120 agent-hours.
2. Agents needed on the phones = 120 / 0.80 = 150.
3. Roster = 150 / (1 - 0.30) = 214.29, round up to 215.
**Result:** 215 agents rostered (150 productive at the desk).
**Check:** 215 x 0.7 = 150.5 available; x 0.8 = 120.4 hours of work capacity, at least 120.
**Caveats:** Real centres use Erlang C to meet a wait-time target (such as 80% of calls in 20 seconds); this simple method understates staff needed when calls arrive in bursts.
**Likely follow-ups:** 1) *AHT drops to 5 minutes?* 100 / 0.8 / 0.7 = 178.6, so 179. 2) *Why not divide by 0.3 shrinkage?* It is a loss rate, so use 1 minus it.
**Common mistakes / traps:** Multiplying by 1.3 instead of dividing by 0.7; skipping occupancy (assuming 100% busy); treating 6 min as 0.6 hours.

### Q34 ⭐⭐ 🟡 A ride-hailing city sees 600,000 completed rides a day. A cab completes 14 rides a day and is on the road (available) 80% of the fleet at any time. How many cabs must be registered?
**Given:** 600,000 rides/day; 14 rides per active cab per day; only 80% of registered cabs are active on a day.
**Asked at:** commonly asked (no company-specific report found); gap-fill fleet-sizing calculation.
**What the interviewer is checking:** Chaining demand to active supply, then active to registered supply.
**Say this in the interview:** "600,000 / 14 gives about 42,900 active cabs; divide by 0.8 for the registered fleet: about 53,600."
**Definition in plain words:** Active cabs = rides / rides per cab. Registered cabs = active cabs / active share.
**Worked answer:**
1. Active cabs = 600,000 / 14 = 42,857.
2. Registered = 42,857 / 0.80 = 53,571.4, round up to 53,572.
**Result:** about 53,600 registered cabs (about 10,700 inactive on a given day).
**Check:** 53,572 x 0.8 = 42,858 active; x 14 = 600,001 rides. Matches.
**Caveats:** "Rides per cab" is an average; peak-hour supply is not guaranteed by the daily number (see peak factor). The question mixes "on the road 80% of the fleet at any time" with a per-day active share; I treated it as 80% active, as the given line says.
**Likely follow-ups:** 1) *If rides per cab rise to 16?* 46,875 registered. 2) *Is this enough at peak?* Not necessarily; check peak-hour demand.
**Common mistakes / traps:** Multiplying by 0.8 instead of dividing; treating registered and active as the same.

### Q35 ⭐⭐ 🟡 A parcel hub sorter handles 8,000 items per hour, runs 20 hours a day and achieves 75% utilisation. How many such hubs are needed for 700,000 packages a day?
**Given:** 8,000 items/hour; 20 hours/day; 75% utilisation; 700,000 packages/day; one sorter per hub. Round up.
**Asked at:** commonly asked (no company-specific report found); gap-fill logistics capacity calculation.
**What the interviewer is checking:** Effective capacity = rated capacity x hours x utilisation.
**Say this in the interview:** "One hub sorts 120,000 a day effectively, so 700,000 needs 5.83, so 6 hubs."
**Definition in plain words:** Effective daily capacity = items/hour x hours x utilisation (the share of time it actually works at full speed).
**Worked answer:**
1. Rated capacity per day = 8,000 x 20 = 160,000.
2. Effective = 160,000 x 0.75 = 120,000.
3. Hubs = 700,000 / 120,000 = 5.83, round up to 6.
**Result:** 6 hubs.
**Check:** 6 x 120,000 = 720,000 at least 700,000; 5 hubs give 600,000, not enough.
**Caveats:** The 6th hub would run at 97% of effective capacity (700/720), leaving no slack for peaks; a planner would add a seventh or extend hours.
**Likely follow-ups:** 1) *Utilisation 90%?* Capacity 144,000, so 4.86, so 5 hubs. 2) *Peak season +30%?* 910,000 needs 7.6, so 8 hubs.
**Common mistakes / traps:** Ignoring utilisation; rounding 5.83 down; assuming volume is flat across hours.

### Q36 ⭐⭐ 🟡 A dark store has on average 12 orders in progress and each order takes 8 minutes to pick and pack. By Little's Law, how many orders arrive per hour?
**Given:** average work-in-progress 12 orders; average time in system 8 minutes; steady state.
**Asked at:** commonly asked (no company-specific report found); gap-fill operations-theory calculation.
**What the interviewer is checking:** That you know Little's Law and convert minutes to hours.
**Say this in the interview:** "Little's Law says average orders in the system equals arrival rate times time in system, so rate = 12 / (8/60) = 90 orders an hour."
**Definition in plain words:** Little's Law: L = lambda x W. L is the average number in the system, lambda the arrival rate, W the average time each spends inside. It holds in steady state (arrivals about equal departures).
**Worked answer:**
1. W = 8 minutes = 8/60 = 0.1333 hour.
2. lambda = L / W = 12 / 0.1333 = 90 orders per hour.
**Result:** 90 orders per hour (1.5 per minute).
**Check:** Each order stays 8 minutes, so a "slot" turns over 7.5 times an hour; 12 slots x 7.5 = 90.
**Caveats:** Needs steady state, and "in progress" should cover the same stage as the time (pick and pack only).
**Likely follow-ups:** 1) *If pick time falls to 6 minutes at 90 orders/hour?* L = 90 x 0.1 = 9 orders in progress. 2) *Why useful?* Sizes pickers and bins.
**Common mistakes / traps:** Using 8 instead of 8/60 (giving 1.5); mixing up L and lambda.

### Q37 ⭐⭐ 🟡 An edtech company has 20,000 learners attending live classes. Each learner attends 2 classes a day, a batch holds 40 learners and one teacher can conduct 4 classes a day. How many teachers are needed?
**Given:** 20,000 learners; 2 live classes/learner/day; 40 per batch; 4 classes per teacher per day. Round up.
**Asked at:** commonly asked (no company-specific report found); gap-fill capacity calculation.
**What the interviewer is checking:** Converting learner-classes to class sessions to teachers.
**Say this in the interview:** "40,000 learner-classes, 1,000 classes at 40 per batch, 250 teachers at 4 classes each."
**Definition in plain words:** Teachers = (learners x classes each / batch size) / classes per teacher.
**Worked answer:**
1. Learner-seats needed per day = 20,000 x 2 = 40,000.
2. Classes = 40,000 / 40 = 1,000.
3. Teachers = 1,000 / 4 = 250 exactly (no rounding needed).
**Result:** 250 teachers.
**Check:** 250 x 4 x 40 = 40,000 learner-seats.
**Caveats:** No allowance for leave or absence: at 1 weekly off and 8% absence, roster would be 250 / 0.92 x 7/6 = 317.03, so 318 (my own extension, as in Q32). Batches may be uneven and slots may clash.
**Likely follow-ups:** 1) *Batch size 50?* 800 classes, 200 teachers. 2) *Peak slot problem?* Everyone wants the evening slot, so more teachers are needed there.
**Common mistakes / traps:** Dividing learners by batch size without the 2 classes; forgetting leave cover.

### Q38 ⭐⭐ 🟡 Estimate the number of delivery executives an e-commerce company needs in Hyderabad.
**Asked at:** commonly asked (no company-specific report found); a packages-delivered-per-city prompt for Flipkart appears on a practice site (unverified).
**What the interviewer is checking:** Orders to deliveries per person, then roster gross-up and market share.
**Say this in the interview:** "Parcels per day divided by parcels per executive gives about 3,600 on duty for the whole city, about 4,600 on the roster; one company with 25% share needs about 1,200."
**Clarify first:** Home delivery of parcels (not food), a normal non-sale day, one company with a share of the city market, own or contracted riders counted.
**Approach:** Bottom-up from households, because parcels per household is easy to reason about.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Households in the city | 2.5 million | about 10 million people at 4 per home |
| Parcels per household per month | 1.5 | ordering is occasional |
| Parcels per executive per day | 35 | dense urban route with failed attempts |
| Weekly off | 6 of 7 days worked | usual policy |
| Absenteeism | 10% | assumed |
| Company share | 25% | one of several players |
**Calculation:**
1. Parcels per day (market) = 2.5 million x 1.5 / 30 = 125,000.
2. On duty = 125,000 / 35 = 3,571.
3. Roster = 3,571 x 7/6 / 0.90 = 4,630.
4. Company at 25% share = 4,630 x 0.25 = about 1,160.
**Result:** about 1,200 executives for one company (range 800 to 1,900); about 4,600 for the whole city.
**Sanity check:** 125,000 parcels a day against 10 million people is 1 parcel per 80 people a day, plausible for a big city.
**Sensitivity:** Parcels per executive: at 30 the answer is about 1,350; at 40 about 1,000. Share and household ordering rate scale the answer one-for-one.
**Likely follow-ups:** 1) *Sale day?* Orders 2 to 3 times; a company hires temporary riders. 2) *Why is roster larger?* Weekly offs and absences.
**Common mistakes / traps:** Estimating the whole market and calling it one company's need; forgetting weekly off and absence; mixing food and parcel delivery speeds.

### Q39 ⭐⭐ 🟡 Estimate the daily footfall and revenue of a food court in a large mall.
**Asked at:** commonly asked (no company-specific report found); gap-fill revenue-per-venue prompt.
**What the interviewer is checking:** Funnel from mall visitors to food-court buyers to spend, plus a capacity cross-check.
**Say this in the interview:** "About 3,750 food-court visitors spending ₹300 each, so roughly ₹11 lakh a day."
**Clarify first:** A large city mall, an average day (weekdays and weekend blended), count paying customers, not accompanying family members.
**Approach:** Funnel (top-down), then check against seat capacity (bottom-up).
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Mall footfall | 25,000 a day | large mall, blended days |
| Share who eat at food court | 15% | many come to shop or watch movies |
| Spend per person | ₹300 | quick-service meals |
| Seats | 400 | typical large food court |
| Turns per seat per day | 6 | lunch, evening, dinner |
**Calculation:**
1. Footfall to food court = 25,000 x 15% = 3,750 visitors.
2. Revenue = 3,750 x ₹300 = ₹11.25 lakh.
3. Capacity check: 400 x 6 = 2,400 seated meals, plus takeaway.
**Result:** about 3,750 visitors and ₹11 lakh a day (range ₹8 to 15 lakh).
**Sanity check:** The 2,400 seated meals is lower than 3,750, so about 35% would have to be takeaway or standing, which is believable, or turns are about 9; I would trim the answer toward 3,000 visitors, about ₹9 lakh, if I wanted to respect seats.
**Sensitivity:** Conversion share (15%) is the biggest lever: 10% gives ₹7.5 lakh, 20% gives ₹15 lakh. Spend per head moves it by the same percentage.
**Likely follow-ups:** 1) *Weekend?* Footfall about 2x. 2) *Revenue to the mall?* Often a rent or revenue share.
**Common mistakes / traps:** Assuming every visitor eats; ignoring seat capacity; counting accompanying children as buyers.

### Q40 ⭐⭐ 🟡 Estimate the number of cab rides to and from a metro city airport in a day.
**Asked at:** one candidate report of an Uber revenue from Delhi airport guesstimate at a business analyst interview (Glassdoor, unverified); otherwise commonly asked.
**What the interviewer is checking:** Passenger flow, mode share and passengers per cab.
**Say this in the interview:** "About 80,000 airport passengers a day; 30% by app cab at 2 per cab gives about 12,000 rides, range 8,000 to 19,000."
**Clarify first:** App-based and taxi cabs together, one-way trips counted separately (to and from), passengers only (not staff or meeters).
**Approach:** Top-down from daily passengers and mode share; cross-check by the cab queue rate.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Passengers a day (arrivals + departures) | 80,000 | large metro airport |
| Share going by cab | 30% | rest use own car, metro, bus |
| Passengers per cab | 2 | some travel alone, some in groups |
**Calculation:**
1. Cab passengers = 80,000 x 30% = 24,000.
2. Rides = 24,000 / 2 = 12,000 per day (about 6,000 to the airport and 6,000 from it).
**Result:** about 12,000 rides a day (low 7,500 at 60,000 pax, 25% and 2; high 19,400 at 100,000 pax, 35% and 1.8).
**Sanity check:** 12,000 rides over about 18 busy hours is about 670 an hour, or about 11 cabs a minute; plausible for a big terminal.
**Sensitivity:** Passenger count and cab share both scale the answer proportionally; a 5-point change in cab share (25% to 35%) moves it from 10,000 to 14,000.
**Likely follow-ups:** 1) *Revenue?* At an assumed ₹600 per ride, 12,000 rides is ₹72 lakh a day. 2) *Peak?* Early morning and late evening banks of flights.
**Common mistakes / traps:** Counting only departures; treating each passenger as a ride; ignoring staff and cargo traffic.

### Q41 ⭐⭐ 🟡 Estimate the monthly loan processing-fee revenue of a digital lending app in one city.
**Asked at:** commonly asked (no company-specific report found); gap-fill fintech prompt.
**What the interviewer is checking:** A funnel from population to disbursed loans to fee income, and awareness that fees are a share of loan value.
**Say this in the interview:** "About 2,200 loans a month at ₹25,000 and a 2% fee gives roughly ₹11 lakh in fees."
**Clarify first:** One app, a city of about 6 million people, new loans disbursed in a month, processing fee only (not interest).
**Approach:** Top-down funnel with the app's market share.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| City population | 6 million | large city |
| Adults | 60% | age structure |
| Adults eligible and digitally active | 40% of adults | income, smartphone, credit history |
| Eligible who take a digital loan in a month | 1% | occasional borrowing |
| App share of those loans | 15% | one of many apps |
| Average loan | ₹25,000 | small-ticket loans |
| Processing fee | 2% | assumed (fees vary) |
**Calculation:**
1. Adults = 6 million x 60% = 3.6 million; eligible = 3.6 million x 40% = 1.44 million.
2. Market loans per month = 1.44 million x 1% = 14,400.
3. The app's loans = 14,400 x 15% = 2,160.
4. Fee per loan = 25,000 x 2% = ₹500.
5. Revenue = 2,160 x 500 = ₹10.8 lakh.
**Result:** about ₹11 lakh a month (range ₹6 to 27 lakh).
**Sanity check:** 2,160 loans a month is 72 a day for a 6-million city, a small share, so it feels modest.
**Sensitivity:** Monthly take-up (1%) and app share (15%) multiply directly: take-up 0.5% to 2% moves revenue from about ₹5 to 22 lakh.
**Likely follow-ups:** 1) *Why not interest income?* Question asks fees; interest arrives over months and needs default assumptions. 2) *What about rejection?* Apply an approval rate: only approved loans pay a fee.
**Common mistakes / traps:** Counting applications as disbursals; assuming a fee on the whole population; forgetting that fee income arrives upfront while default cost comes later.

### Q42 ⭐⭐ 🟡 Estimate the number of orders an Indian quick-commerce app gets in a single city on a rainy day versus a normal day, and say which assumptions change.
**Asked at:** commonly asked (no company-specific report found); quick-commerce daily-orders prompts for Blinkit-type apps appear on candidate sites (unverified).
**What the interviewer is checking:** That demand and supply are separate, and orders fulfilled is capped by the smaller of the two.
**Say this in the interview:** "Normal day about 36,000 orders; on a rainy day demand may rise about 30% to 47,000 but riders and speed fall, so fulfilled orders are only about 37,000."
**Clarify first:** One city of 12 million, one app, a normal weekday vs a heavy-rain weekday, count completed orders.
**Approach:** Bottom-up demand from households; then apply a supply cap.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Households | 3 million | 12 million people / 4 |
| Active monthly user households | 6% | one app in one city |
| Orders per active household per month | 6 | assumed |
| Normal capacity utilisation | 70% | some headroom |
| Rain: demand uplift | +30% | people avoid going out |
| Rain: rider availability | 85% of normal | some stay off the road |
| Rain: delivery speed | 85% of normal | slower trips |
**Calculation:**
1. Normal orders = 3 million x 6% x 6 / 30 = 36,000 per day.
2. Capacity = normal / 0.70 = 51,400 per day.
3. Rain demand = 36,000 x 1.3 = 46,800.
4. Rain capacity = 51,400 x 0.85 x 0.85 = 37,200.
5. Fulfilled = min(46,800, 37,200) = about 37,200; unmet demand about 9,600.
**Result:** normal about 36,000; rainy day demand about 47,000 but about 37,000 fulfilled (range 30,000 to 47,000).
**Sanity check:** Fulfilled is about 3% above normal, consistent with the app being near capacity both days; the gap shows up as cancellations, long waits and surge fees.
**Sensitivity:** Rain capacity: if riders only fall to 95%, fulfilled rises to about 41,500; if they fall to 70%, about 30,600. Normal utilisation (headroom) also matters.
**Likely follow-ups:** 1) *Which assumptions change?* Demand uplift, rider supply, speed, basket size. 2) *How would you validate?* Compare past rainy days in order logs.
**Common mistakes / traps:** Raising orders by a demand factor only; forgetting supply constraints; not stating that rain affects only some hours.

### Q43 ⭐⭐ 🟡 After you give your Swiggy orders estimate, the interviewer says a public figure is 10 times higher. What do you do?
**Asked at:** a candidate report of a Swiggy orders-per-day guesstimate on a Board Infinity forum (unverified); the pushback itself is commonly asked.
**What the interviewer is checking:** Calm, structured reasoning when challenged, not defensiveness or instant surrender.
**Say this in the interview:** "A 10x gap tells me a structural assumption is wrong, so I would first check scope and units, then find which input could explain a factor of 10."
**Explain simply:**
- Step 1: do not panic and do not just multiply by 10. Thank them and ask what the public figure measures: orders or GMV, a day or a month, food only or also grocery, India or one city.
- Step 2: line up scope. A 10x gap often comes from a unit mismatch: monthly vs daily is about 30x; revenue vs orders; users vs orders.
- Step 3: reconcile my chain. Example (assumed): my chain was 1.4 billion x 1% active x 1 order a week / 7 = 0.2 million a day. A factor 10 could mean 10% active users, or 3 orders a week, or more cities than I assumed. Ask which is more plausible (3 orders a week per active user is possible; 10% of India ordering is not).
- Step 4: update openly. "If the figure is food orders per day nationwide, I would raise active users and frequency, giving about X; here is my new range."
- Step 5: if I still disagree and the figure is unverified, say so politely and explain what I can check.
- Practice step: take any estimate and write down three inputs that could each explain a 10x gap.
**Likely follow-ups:** 1) *What if you cannot find the cause?* Present both and the range between. 2) *Is a large miss a failure?* Not if the structure is sound and you adapt.
**Common mistakes / traps:** Defending a number out of ego; scaling by 10 without finding why; skipping the units and scope question.

### Q44 ⭐⭐ 🟡 Which assumption in a rider-fleet guesstimate would you test first with sensitivity analysis, and how would you do it?
**Asked at:** a Zomato rider fleet in Bengaluru prompt appears on a practice site (unverified); the sensitivity question itself is commonly asked.
**What the interviewer is checking:** That you know which inputs drive the answer, not just that you can calculate it.
**Say this in the interview:** "I would test orders per rider per hour first, because the fleet is inversely proportional to it and it is the least certain input."
**Explain simply:**
- Sensitivity analysis: change one input at a time by the same percentage (say plus or minus 25%) and see how much the answer moves. The input with the biggest swing deserves the most care.
- Fleet = orders x peak share / orders per rider per hour x roster factor. Orders, peak share and roster factor move the answer one-for-one; rider productivity moves it inversely, and is the shakiest input.
- Worked example (assumed base): 60,000 orders a day, 12% in the peak hour, 2.5 orders per rider per hour, roster factor 1.4. Base = 60,000 x 0.12 / 2.5 x 1.4 = 4,032 riders.
- Productivity 2.0: 5,040 (+25%); productivity 3.0: 3,360 (-17%). Peak share 15%: 5,040 (+25%). Roster factor 1.2: 3,456 (-14%).
- Method in Excel: put inputs in cells, change one at a time, record the output, and rank in a table (a tornado chart for presentation).
- Practice step: do the same with an assumed order count of 80,000 and note which input still dominates.
**Likely follow-ups:** 1) *Why not just trust the average?* Productivity varies with traffic and distance. 2) *How would you check real values?* Pull rider logs.
**Common mistakes / traps:** Changing several inputs at once; testing a tiny input; presenting the sensitivities without a decision.

### Q45 ⭐⭐ 🟡 How would you present a revenue guesstimate as a low-base-high range instead of a single number?
**Asked at:** commonly asked (no company-specific report found); gap-fill structured-thinking question.
**What the interviewer is checking:** That you communicate uncertainty honestly and tie the range to specific assumptions.
**Say this in the interview:** "I would give base, low and high cases by moving only the shakiest two or three inputs, and say what each case means."
**Explain simply:**
- Step 1: build the base case with your best assumptions.
- Step 2: pick the 2 or 3 inputs you are least sure of (usually volume, conversion, price).
- Step 3: set low and high values for each from a realistic reason, not a random plus or minus.
- Step 4: compute the three cases and say what each needs to be true. Do not move every input to its worst value at once (it makes an unrealistic extreme).
- Worked example, multiplex (assumed): base 3,200 tickets at ₹420 per head including F&B = ₹13.4 lakh. Low: occupancy 30%, ₹400 per head = ₹9.6 lakh. High: occupancy 50%, ₹490 per head = ₹19.6 lakh.
- Say it as: "about ₹13 lakh a day, likely between ₹10 and 20 lakh, with occupancy the swing factor."
- Practice step: take any earlier estimate and write low, base, high with one line of reasoning each.
**Likely follow-ups:** 1) *How wide should the range be?* Wide enough to hold the truth most of the time, but not so wide it is useless (within 2x is a common aim). 2) *Which to quote?* Lead with base, then the range.
**Common mistakes / traps:** False precision (₹13,44,000); a range with no stated driver; moving every input to the extreme.

### Q46 ⭐⭐ 🟡 A metro line runs a train every 3 minutes in each direction during the peak. Each train has 6 coaches and each coach carries up to 250 passengers at peak. What is the maximum passengers per direction in one peak hour?
**Given:** one train every 3 minutes per direction; 6 coaches per train; 250 passengers per coach; 60-minute peak hour.
**Asked at:** commonly asked (no company-specific report found); metro riders methods appear on practice blogs (unverified).
**What the interviewer is checking:** Frequency x capacity, and the word "maximum".
**Say this in the interview:** "20 trains an hour, 1,500 passengers each, so a maximum of 30,000 per direction per hour."
**Definition in plain words:** Line capacity per direction = trains per hour x passengers per train (this is the theoretical ceiling, often called PPHPD, passengers per hour per direction).
**Worked answer:**
1. Trains per hour = 60 / 3 = 20.
2. Passengers per train = 6 x 250 = 1,500.
3. Capacity = 20 x 1,500 = 30,000.
**Result:** 30,000 passengers per direction per hour (60,000 across both directions).
**Check:** 30,000 / 60 = 500 passengers per minute; one train of 1,500 every 3 minutes = 500 per minute. Same.
**Caveats:** This is a ceiling at full crush loading; real peaks run lower, trains do not leave exactly every 3 minutes, and stations limit it. A train every 2 minutes would give 45,000.
**Likely follow-ups:** 1) *At 75% load?* 22,500. 2) *At 2.5-minute headway?* 24 trains, 36,000.
**Common mistakes / traps:** Counting both directions together; multiplying coaches by passengers only; calling the ceiling the actual ridership.

### Q47 ⭐⭐ 🟡 Estimate the number of Uber or Ola cabs idle at any moment in a metro city at 3 pm on a weekday.
**Asked at:** commonly asked (no company-specific report found); related ride-hailing guesstimates appear on candidate sites (unverified).
**What the interviewer is checking:** Supply (cabs online) and the busy-versus-idle split at a specific time.
**Say this in the interview:** "About 33,000 cabs are active in a day; at 3 pm perhaps 60% are online and about 35% of those are idle, so roughly 7,000."
**Clarify first:** One big metro (about 12 million people), both apps together, idle means online and waiting without a booking (not on a trip, not offline).
**Approach:** Bottom-up from rides to active fleet, then time-of-day factors.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Rides per day, both apps | 400,000 | large metro |
| Rides per active cab per day | 12 | typical use |
| Share of active cabs online at 3 pm | 60% | lull between peaks |
| Share of online cabs idle at 3 pm | 35% | the rest on trips or heading to pickup |
**Calculation:**
1. Active cabs = 400,000 / 12 = 33,333.
2. Online at 3 pm = 33,333 x 60% = 20,000.
3. Idle = 20,000 x 35% = 7,000.
**Result:** about 7,000 idle cabs (range 4,000 to 10,000).
**Sanity check:** 7,000 idle over 12 million people is about 1 idle cab per 1,700 people, which feels reasonable.
**Sensitivity:** The idle share is the biggest lever: 25% idle gives 5,000, 45% gives 9,000. Online share at 3 pm is next.
**Likely follow-ups:** 1) *How does it differ at 9 am?* More cabs busy, fewer idle. 2) *Why does idle time matter?* It shows oversupply and driver earnings.
**Common mistakes / traps:** Treating the whole fleet as idle; mixing registered with active cabs; ignoring that drivers take breaks at 3 pm.

### Q48 ⭐⭐ 🟡 A food delivery app notices a delivery partner's average cycle time is 28 minutes and a payout of ₹40 per order. What is the payout cost per active hour and how would you use it to judge rider utilisation?
**Given:** 28-minute order cycle; ₹40 payout per order; no idle time.
**Asked at:** commonly asked (no company-specific report found); gap-fill rider-economics calculation.
**What the interviewer is checking:** Orders per hour from cycle time, earnings per hour, and a sensible use of the number as a benchmark.
**Say this in the interview:** "60 divided by 28 is 2.14 orders an hour, so ₹40 x 2.14 = about ₹86 per active hour at full utilisation; real utilisation is actual orders per hour compared with 2.14."
**Definition in plain words:** Cycle time is the full time from accepting an order to being free for the next one. Orders per hour = 60 / cycle time. Payout per active hour = payout per order x orders per hour. Utilisation = actual orders per hour / maximum orders per hour.
**Worked answer:**
1. Orders per hour = 60 / 28 = 2.143.
2. Payout per hour = 2.143 x ₹40 = ₹85.71.
3. Use as a benchmark: "no idle time" is the ceiling. If a rider really completes 1.5 orders per hour, utilisation = 1.5 / 2.143 = 70% and the rider earns ₹60 per hour logged in.
**Result:** about ₹86 per active hour at 100% utilisation; at 50% it is about ₹43, at 70% ₹60, at 90% ₹77.
**Check:** 28 minutes x 2.143 = 60 minutes. Matches.
**Caveats:** Cycle time includes waiting at the restaurant; zero idle time never happens in practice. Payout is per order, so cost per order stays ₹40 whatever utilisation; low utilisation hurts the rider and wastes capacity, and raises cost only if the app pays a guaranteed hourly minimum.
**Likely follow-ups:** 1) *Why does it matter to the company?* Low utilisation means too many riders for the demand. 2) *How would you raise it?* Batch orders, shorten restaurant wait, shift incentives to peak.
**Common mistakes / traps:** Dividing 28 by 60 the wrong way round; treating the ₹86 as what riders actually earn; ignoring idle time.

### Q49 ⭐⭐ 🟡 A metro station gate processes 30 passengers per minute per gate. A station needs to clear 9,000 passengers in a peak hour. How many gates are needed?
**Given:** 30 passengers/minute/gate; 9,000 passengers in 60 minutes; assume gates are fully used. Round up.
**Asked at:** commonly asked (no company-specific report found); a capacity-sizing calculation of the kind used in operations guesstimate rounds (gap-fill, unverified).
**What the interviewer is checking:** Whether you convert everything to one time unit first, divide cleanly and round up.
**Say this in the interview:** "9,000 an hour is 150 a minute; each gate does 30 a minute, so 5 gates exactly. In real life I would add one spare for the peak-of-the-peak."
**Definition in plain words:** Capacity needed divided by capacity of one unit, rounded up. Gates = demand per minute / throughput per gate per minute.
**Worked answer:**
1. Demand per minute = 9,000 / 60 = 150 passengers per minute.
2. Gates = 150 / 30 = 5.
**Result:** 5 gates (exactly full, no slack). With one spare for breakdowns or surges, 6.
**Check:** 5 gates x 30 x 60 minutes = 9,000, matches demand. 4 gates would clear only 7,200, leaving 1,800 people queuing.
**Caveats:** Arrivals are not even across the hour (a train dumps a crowd in 30 seconds), so a real design uses the busiest 5-minute window, not the hourly average. Gates are also used in one direction at a time.
**Likely follow-ups:** 1) *If the rate drops to 25 a minute?* 150/25 = 6 gates. 2) *What if the peak is 20% higher?* 10,800 an hour = 180 a minute, so 6 gates.
**Common mistakes / traps:** Mixing hours with minutes (9,000/30 = 300 gates); forgetting to round up; leaving zero spare capacity.

### Q50 ⭐⭐ 🟡 A hub's trucks each carry 400 parcels and make 3 trips a day. How many trucks are needed for 90,000 parcels a day, if 10% of trucks are off the road for maintenance?
**Given:** 400 parcels/trip; 3 trips/truck/day; 90,000 parcels/day; 10% of fleet unavailable. Round up.
**Asked at:** commonly asked (no company-specific report found); logistics fleet-sizing is a common operations calculation (gap-fill, unverified).
**What the interviewer is checking:** Whether you size the trucks on the road first and then gross up for the trucks that are unavailable.
**Say this in the interview:** "One truck moves 1,200 parcels a day, so 75 trucks must be running. Only 90% of the fleet is available, so I divide 75 by 0.9 and round up to 84."
**Definition in plain words:** Fleet = trucks needed on the road / share of fleet available. Trucks on the road = daily parcels / (parcels per trip x trips per day).
**Worked answer:**
1. Parcels per truck per day = 400 x 3 = 1,200.
2. Trucks on the road = 90,000 / 1,200 = 75.
3. Available share = 100% - 10% = 90%, so fleet = 75 / 0.9 = 83.3, round up to 84.
**Result:** 84 trucks.
**Check:** 84 x 0.9 = 75.6 available trucks, enough for 75. With 83 trucks, 83 x 0.9 = 74.7, which falls short.
**Caveats:** Assumes every trip is completely full (400) and trips are perfectly spread. Real load factors are about 80-90%, which would raise the fleet.
**Likely follow-ups:** 1) *If trucks are only 80% full?* 75 / 0.8 = 94 on the road, then 94 / 0.9 = 104.2, so 105. 2) *What if unavailability is 15%?* 75 / 0.85 = 88.2, so 89.
**Common mistakes / traps:** Adding 10% to 75 (75 x 1.1 = 82.5, rounds to 83, which is short because 10% of the bigger fleet is the off-road share, not 10% of 75); forgetting the 3 trips.

### Q51 ⭐⭐ 🟡 Estimate the daily revenue of a mid-sized Indian restaurant that lists on a delivery app, split between dine-in and delivery.
**Asked at:** commonly asked (no company-specific report found); revenue-per-venue estimates are a standard guesstimate type (gap-fill, unverified).
**What the interviewer is checking:** Whether you split the business into two channels with different volumes and bill values, and separate gross sales from what the restaurant keeps.
**Say this in the interview:** "I will build it bottom-up: dine-in covers times average bill, plus delivery orders times average bill. I get about Rs 52,000 a day gross, of which delivery is about 30%."
**Clarify first:** City tier (assume a metro), type (mid-priced casual dining, around 60 seats), and whether "revenue" means gross sales or what the restaurant keeps after app commission. I will show both.
**Approach:** Bottom-up by channel, because dine-in depends on seats and turns while delivery depends on app orders.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Dine-in covers per day | 80 | 60 seats, about 1.3 turns across lunch and dinner |
| Dine-in spend per person | Rs 450 | mid-priced casual restaurant |
| Delivery orders per day | 45 | steady listing on one or two apps |
| Delivery order value | Rs 350 | single or couple meal |
| App commission | 25% | assumed typical range 20-30% |
**Calculation:**
1. Dine-in = 80 x 450 = Rs 36,000.
2. Delivery gross = 45 x 350 = Rs 15,750.
3. Total gross = 36,000 + 15,750 = Rs 51,750 (delivery share about 30%).
4. Commission = 25% of 15,750 = Rs 3,938, so delivery net = Rs 11,812.
5. Net of commission total = Rs 47,812.
**Result:** About Rs 50,000 a day gross (range Rs 30,000-80,000); about Rs 48,000 after app commission.
**Sanity check:** Rs 52,000 x 365 = about Rs 1.9 crore a year, plausible for a busy 60-seat restaurant in a metro.
**Sensitivity:** Dine-in covers matter most. 20% more covers adds Rs 7,200 (14%), while 20% more delivery orders adds only Rs 3,150.
**Likely follow-ups:** 1) *Weekend vs weekday?* Weekend dine-in perhaps 1.5x. 2) *Is delivery profitable after commission?* Not necessarily; food cost and packaging come out of the 75% the restaurant keeps.
**Common mistakes / traps:** Counting delivery at the app's customer price including delivery fee and taxes; ignoring commission; using seats times price with no turns assumption.

### Q52 ⭐⭐ 🔴 Estimate the annual advertising revenue of a large metro rail network.
**Asked at:** commonly asked (no company-specific report found); the Delhi Metro ridership guesstimate appears on prep sites, this advertising variant is a gap-fill (unverified).
**What the interviewer is checking:** Whether you can list the ad inventory (places where ads can sit), price each, and allow for unsold space.
**Say this in the interview:** "I split ad inventory into stations, trains and other, price each and apply an occupancy rate. I get about Rs 150 crore a year, roughly 80 paise per rider."
**Clarify first:** Network size (assume a large network, about 250 stations and 300 train sets), and revenue means ad contract revenue to the metro company, not agency billings.
**Approach:** Bottom-up by inventory type, then a per-rider cross-check.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Stations | 250 | large network |
| Ad panels per station | 40 | platform, concourse, pillars, gate panels |
| Rate per panel | Rs 15,000/month | average of premium and ordinary sites |
| Occupancy | 60% | some space unsold |
| Train sets | 300 | with wraps and interior panels |
| Revenue per train set | Rs 10 lakh/year | wrap plus interior ads |
| Other (naming rights, digital screens, tickets/cards) | Rs 15 crore | small extras |
**Calculation:**
1. Station ads = 250 x 40 x 15,000 x 12 x 0.6 = Rs 108 crore.
2. Train ads = 300 x 10 lakh = Rs 30 crore.
3. Other = Rs 15 crore.
4. Total = 108 + 30 + 15 = Rs 153 crore.
**Result:** About Rs 150 crore a year (plausible range Rs 80-250 crore).
**Sanity check:** Assume 5 million riders a day x 365 = 1.8 billion rides; Rs 153 crore / 1.8 billion = about Rs 0.84 per ride. Small per rider, which is believable for ads.
**Sensitivity:** Occupancy and rate per panel move station ads directly: 40% occupancy gives Rs 72 crore, 80% gives Rs 144 crore, a swing of Rs 72 crore on its own.
**Likely follow-ups:** 1) *Which stations earn most?* Interchange and central business district stations. 2) *Would you add digital screens?* Yes, higher rate per slot but shared by several advertisers.
**Common mistakes / traps:** Assuming 100% of space is sold; ignoring that rates vary 10x between stations; mixing ad revenue with fare revenue.

### Q53 ⭐⭐ 🔴 Estimate the number of orders a food delivery app receives in one city during an IPL final evening, and explain how you model the event spike.
**Asked at:** commonly asked (no company-specific report found); prep sites list sale-day and Sunday-order estimation prompts of this shape, unverified.
**What the interviewer is checking:** Whether you start from a normal-day baseline and apply hour-by-hour multipliers instead of guessing a big number.
**Say this in the interview:** "I take a normal evening as the baseline, then multiply each hour by an event factor tied to the match stages. I get roughly 1.45 times a normal evening, about 217,000 orders."
**Clarify first:** One city (assume Bengaluru), one app, evening means 6 pm to midnight, match starts at 7:30 pm and ends about 11 pm.
**Approach:** Baseline by hour (top-down from daily orders), then event multipliers by phase of the match. I use the baseline-times-multiplier idea because it is easy to defend line by line.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| App orders in the city per normal day | 300,000 | large metro, leading app |
| Share in the 6 pm-midnight window | 50% = 150,000 | dinner-heavy day |
| Hourly shape (6 to 12) | 14%, 16%, 18%, 18%, 18%, 16% | ramp into dinner |
| Event multipliers (same hours) | 1.1, 1.5, 1.6, 1.5, 1.7, 1.2 | pre-match build-up, mid-match snacks, final-over and post-match |
**Calculation:**
1. Baseline per hour: 21,000; 24,000; 27,000; 27,000; 27,000; 24,000.
2. With multipliers: 23,100; 36,000; 43,200; 40,500; 45,900; 28,800.
3. Sum = 217,500 orders in the evening.
4. Ratio to normal = 217,500 / 150,000 = 1.45.
5. Busiest hour (10-11 pm) = 45,900, about 12.8 orders a second.
**Result:** About 217,000 evening orders (range 180,000-260,000); about 370,000 for the whole day, up about 22%.
**Sanity check:** Evening-only uplift 45% means the full-day uplift is 22.5% (67,500 / 300,000), a believable bump for one night.
**Sensitivity:** The multiplier in the busiest hours matters most. If every multiplier is 0.2 lower, the total falls to about 187,500.
**Likely follow-ups:** 1) *What limits the spike?* Rider supply and kitchen capacity, so fulfilled orders may cap below demand. 2) *How would you check it?* Compare with last year's final and a normal Sunday in the data.
**Common mistakes / traps:** Applying one flat multiplier to the whole day; ignoring that orders dip during the key overs and surge at breaks; forgetting rider capacity.

### Q54 ⭐⭐ 🔴 A food delivery platform has 1.5 million orders a day, 25% net revenue take rate, ₹400 AOV and delivery cost of ₹55 per order plus other costs of ₹30 per order. Is it profitable per order, and what is the contribution per order?
**Given:** AOV ₹400; net revenue 25% of GMV; rider cost ₹55/order; other variable costs ₹30/order.
**Asked at:** commonly asked (no company-specific report found); unit-economics calculations are standard in food-delivery case rounds (gap-fill, unverified).
**What the interviewer is checking:** Whether you compute contribution margin per order correctly and note it is not the same as profit after fixed costs.
**Say this in the interview:** "Net revenue is 25% of Rs 400, which is Rs 100. Costs are Rs 85. Contribution is Rs 15 an order, so yes, positive before fixed costs; that is Rs 2.25 crore a day."
**Definition in plain words:** AOV is average order value (what the customer's basket is worth). GMV is the total value of orders. Contribution per order = net revenue per order minus variable costs per order.
**Worked answer:**
1. GMV per day = 1,500,000 x 400 = Rs 60 crore.
2. Net revenue per order = 25% x 400 = Rs 100.
3. Variable costs = 55 + 30 = Rs 85.
4. Contribution per order = 100 - 85 = Rs 15.
5. Daily contribution = 1.5 million x 15 = Rs 2.25 crore (about Rs 821 crore a year, for 365 days).
**Result:** Rs 15 per order, 3.75% of GMV, or 15% of net revenue. Positive per order.
**Check:** 3.75% x 60 crore = Rs 2.25 crore, matches. Break-even rider cost = 100 - 30 = Rs 70 per order; above that, each order loses money.
**Caveats:** The question gives no fixed costs (technology, corporate staff, marketing, customer discounts), so "profitable" means contribution-positive, not profit-positive. A 25% take rate is high for a platform with commission only; it presumably includes delivery fees and ad income. Each 1 percentage point of take rate is worth Rs 4 per order.
**Likely follow-ups:** 1) *If rider cost rises to Rs 70?* Contribution falls to Rs 0. 2) *If AOV rises to Rs 450?* Net revenue Rs 112.5, contribution Rs 27.5.
**Common mistakes / traps:** Using GMV as revenue (Rs 400 minus Rs 85); calling Rs 15 per order "profit"; forgetting to multiply by 1.5 million.

### Q55 ⭐⭐ 🔴 Estimate the peak orders per second an e-commerce platform must handle on sale day, and how that differs from the average per second.
**Asked at:** prep sites list sale-day order estimation for Flipkart (Big Billion Days) as a candidate-style prompt, unverified; no company-verified report found.
**What the interviewer is checking:** Whether you know that peaks are many times the average and size for the peak with headroom.
**Say this in the interview:** "A 12 million order day averages 139 orders a second, but the busiest minute is around 600 a second, so I would size for about 1,200 with headroom."
**Clarify first:** Orders placed (checkouts), not page visits; one sale day; assume 12 million orders that day.
**Approach:** Top-down: daily orders, then peak-hour share, then peak-minute factor, then headroom.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Orders on sale day | 12 million | large platform, big sale |
| Share in busiest hour | 12% | midnight or evening launch of deals |
| Busiest minute vs hourly average | 1.5x | deals open on the hour |
| Safety headroom | 2x | systems must not fall over |
**Calculation:**
1. Average = 12,000,000 / 86,400 seconds = 139 orders a second.
2. Busiest hour = 12% x 12 million = 1.44 million; per second = 1,440,000 / 3,600 = 400.
3. Busiest minute = 400 x 1.5 = 600 a second.
4. Design capacity = 600 x 2 = 1,200 a second.
**Result:** Average about 140/s; peak about 600/s (4.3 times average); design target about 1,200/s (8.6 times average). Range for peak: 400-900/s.
**Sanity check:** Peak-hour share of 12% means a flat day would give 4.2% (1/24) per hour, so the peak hour is 2.9 times a flat hour, a typical size for a sale.
**Sensitivity:** Peak-hour share drives it. At 8% the peak minute is 400/s; at 16% it is 800/s.
**Likely follow-ups:** 1) *Why is browsing harder than ordering?* Each order comes with perhaps 50-100 page views and searches, so read traffic is far bigger. 2) *Does stock matter?* Yes, a flash deal on limited stock concentrates demand in seconds.
**Common mistakes / traps:** Designing for the average per second; confusing orders with requests; forgetting that all customers share one clock in India, so there is no natural spread of demand across time zones.

### Q56 ⭐⭐ 🔴 Estimate the revenue a quick-commerce company earns per day across India, stating separately the GMV, take-rate and other-income assumptions.
**Asked at:** prep sites list "estimate daily orders for Blinkit in Delhi" style prompts (product roles, unverified); this revenue variant is a gap-fill.
**What the interviewer is checking:** Whether you separate GMV (sales value) from revenue and list each income stream with its own assumption.
**Say this in the interview:** "Orders times basket gives GMV of about Rs 250 crore a day for the sector; commission and margin of 18% gives Rs 45 crore; ads and fees add Rs 15 crore, so about Rs 60 crore of revenue a day."
**Clarify first:** One company or the whole sector (I take the sector), revenue meaning net revenue not GMV, and marketplace accounting (revenue is the platform's share, not full basket value).
**Approach:** Top-down from orders: GMV, then take rate, then other income.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Orders per day (sector, India) | 5 million | metros and large cities |
| Average order value | Rs 500 | grocery top-ups |
| Take rate (commission and margin on goods) | 18% of GMV | assumed range 15-22% |
| Advertising income | 4% of GMV | brand placement on the app |
| Fees (delivery, handling, small-cart) | Rs 10 per order | partly waived |
**Calculation:**
1. GMV = 5,000,000 x 500 = Rs 2,500 million = Rs 250 crore.
2. Take-rate revenue = 18% x 250 = Rs 45 crore.
3. Ad income = 4% x 250 = Rs 10 crore.
4. Fee income = 5,000,000 x 10 = Rs 5 crore.
5. Total = 45 + 10 + 5 = Rs 60 crore a day.
**Result:** About Rs 60 crore a day (range Rs 35-90 crore), about 24% of GMV; about Rs 22,000 crore a year.
**Sanity check:** Revenue per order = 60 crore / 5 million = Rs 120, which is 24% of the Rs 500 basket. Plausible if the platform keeps a high share, but I would flag it as the first number to challenge.
**Sensitivity:** Orders per day and take rate. 4 million orders gives Rs 48 crore; take rate at 15% gives Rs 52.5 crore.
**Likely follow-ups:** 1) *Why not use full GMV as revenue?* Most of GMV goes to suppliers. 2) *Which stream is fastest growing?* Usually ad income.
**Common mistakes / traps:** Reporting GMV as revenue; adding a delivery fee and commission twice; mixing own-inventory (full sales as revenue) and marketplace models.

### Q57 ⭐⭐ 🔴 Estimate the number of delivery riders in India working for food delivery and quick-commerce apps in a day.
**Asked at:** prep sites list a Zomato rider-fleet-in-Bengaluru prompt (candidate-style, unverified); this India-wide version is a gap-fill.
**What the interviewer is checking:** Whether you use orders divided by orders per rider and handle double-counting of riders working for several apps.
**Say this in the interview:** "Orders per day divided by orders each rider completes. Food gives about 330,000 riders, quick commerce about 280,000, so roughly 520,000 distinct riders after removing overlap."
**Clarify first:** Active riders on a typical day (not registered riders), riders on a bike or cycle, the whole country.
**Approach:** Top-down: orders per segment divided by productivity per rider, then adjust for overlap.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Food orders per day (India) | 4 million | metro and tier-2 |
| Orders per food rider per day | 12 | about 8 hours, 1 order per 40 minutes |
| Quick-commerce orders per day | 5 million | short trips |
| Orders per QC rider per day | 18 | trips of 10-15 minutes |
| Riders working on both kinds of app | 15% of the total | multi-apping |
**Calculation:**
1. Food riders = 4,000,000 / 12 = 333,000.
2. QC riders = 5,000,000 / 18 = 278,000.
3. Sum = 611,000.
4. Remove overlap: 611,000 x 0.85 = 519,000.
**Result:** About 520,000 riders working on a day (range 400,000-800,000).
**Sanity check:** Peak need: if 40% of daily orders fall in the two meal peaks, riders needed on the road at once would be a few hundred thousand, similar to the daily figure because most work in a single shift.
**Sensitivity:** Orders per rider. At 15 food and 22 QC orders per rider, the answer drops to about 400,000.
**Likely follow-ups:** 1) *Registered vs active?* Registered is typically 2-3x active because of churn. 2) *Part-timers?* If half work 4-hour shifts, headcount rises.
**Common mistakes / traps:** Dividing by orders per hour and ignoring shift length; counting the same rider twice; mixing registered riders with daily active.

### Q58 ⭐⭐ 🔴 Estimate the number of ride-hailing trips and total fare revenue in a metro city in a day, then explain how you would split it between two competing apps.
**Asked at:** one Glassdoor candidate report (a 2026 business analyst interview, via search summary, unverified) mentions an Uber revenue guesstimate from Delhi airport; no report found for this exact prompt.
**What the interviewer is checking:** Whether you size trips by users and frequency, price by vehicle type, and split by a reasoned share rule, not a coin toss.
**Say this in the interview:** "About 13 million people, a quarter use ride-hailing, 8 rides a month each, so roughly 870,000 trips a day at about Rs 150 average fare, around Rs 13 crore a day. I would split between the apps by users times usage, adjusted for double usage."
**Clarify first:** City (assume Bengaluru-size, 13 million people), all vehicle types on apps (cab, auto, bike taxi), fare means gross fare paid, not platform revenue.
**Approach:** Bottom-up from users and frequency, price by mix; then a share rule.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 13 million | large metro |
| Ride-hailing users | 25% = 3.25 million | monthly active |
| Rides per user per month | 8 | mix of commuters and occasional users |
| Mix: cab / auto / bike | 35% / 40% / 25% | |
| Average fare: cab / auto / bike | Rs 250 / 120 / 60 | |
**Calculation:**
1. Rides per month = 3.25 million x 8 = 26 million; per day = 26/30 = 867,000.
2. Average fare = 0.35 x 250 + 0.40 x 120 + 0.25 x 60 = 87.5 + 48 + 15 = Rs 150.5.
3. Fare revenue = 867,000 x 150.5 = Rs 13.0 crore a day.
4. Split: if App A has 60% of trips, it carries 520,000 trips and Rs 7.8 crore; App B has 347,000 trips and Rs 5.2 crore.
**Result:** About 870,000 trips and Rs 13 crore a day (range 500,000-1.3 million trips). Split by share of trips, 60/40 as an example.
**Sanity check:** 870,000 trips among 13 million people is 1 trip per 15 people per day, plausible. Cross-check by supply: 100,000 drivers x 8 trips = 800,000.
**Sensitivity:** Users and frequency multiply, so 30% users instead of 25% is 20% more trips. The vehicle mix swings revenue (more bikes lowers it).
**Likely follow-ups:** 1) *How to split?* Use app-install share times rides per user; correct for users who have both apps (multi-homing), which would otherwise be double counted. 2) *Platform revenue?* Fares x commission of about 20% would be about Rs 2.6 crore.
**Common mistakes / traps:** Splitting 50/50 with no reason; counting a multi-app user in both; reporting fares as platform revenue.

### Q59 ⭐ 🟢 Estimate the daily number of couriers who use the metro to carry parcels, if you were sizing a parcel-by-metro pilot.
**Asked at:** commonly asked (no company-specific report found); a niche variant of the metro-riders guesstimate, unverified.
**What the interviewer is checking:** Whether you narrow a big ridership number to a small segment with two independent routes.
**Say this in the interview:** "Two routes: 5 million daily riders times a tiny courier share, and the city's delivery workforce times the share who use the metro. Both give about 5,000 couriers a day."
**Clarify first:** One city's network, couriers meaning gig or company delivery workers carrying parcels (not personal luggage), a typical weekday.
**Approach:** Top-down from ridership; bottom-up from the courier workforce as a cross-check.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Daily metro riders | 5 million | large network |
| Share who are couriers carrying parcels | 0.15% | very small, a few in a thousand |
| Parcel and delivery workers in the city | 150,000 | gig and company riders |
| Share using metro for part of the route | 3% | most use bikes |
**Calculation:**
1. Top-down: 5,000,000 x 0.0015 = 7,500 couriers.
2. Bottom-up: 150,000 x 0.03 = 4,500 couriers.
3. Average of the two is about 6,000; I quote 5,000-7,500.
**Result:** About 5,000-7,500 couriers a day (point estimate 6,000), range 2,000-10,000.
**Sanity check:** 6,000 couriers is 0.12% of riders, so you would meet about one in every 800 passengers; plausible.
**Sensitivity:** The share inputs dominate; doubling either share doubles the answer.
**Likely follow-ups:** 1) *What would the pilot need?* Rules on bag size, off-peak timing and station lockers. 2) *Which line first?* The one linking the biggest warehouses to dense residential areas.
**Common mistakes / traps:** Using total riders as the answer; ignoring that most couriers use bikes; skipping a second route.

### Q60 ⭐ 🟢 Estimate the number of orders an average Swiggy restaurant partner receives in a day, and use it to cross-check the platform total.
**Asked at:** a Board Infinity candidate report (via search summary, unverified) mentions "how many orders does Swiggy get in a day" using population and orders per person; this per-restaurant version is a gap-fill.
**What the interviewer is checking:** Whether you can reach the same number from two directions and show they agree.
**Say this in the interview:** "Bottom-up a restaurant sees about 9 orders a day on the app; top-down 1.8 million orders over 200,000 restaurants is also 9. The two routes agree."
**Clarify first:** Average over all active partners (not a chain outlet), orders on this one app, a normal day.
**Approach:** Per-restaurant bottom-up, then top-down from the platform total.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Orders per restaurant per day (all channels) | 60 | includes small outlets |
| Share that is delivery | 25% | assumed |
| Share of delivery on this app | 60% | two main apps |
| Platform orders per day | 1.8 million | assumed |
| Active restaurant partners | 200,000 | assumed |
**Calculation:**
1. Bottom-up: 60 x 0.25 = 15 delivery orders; x 0.6 = 9 orders on this app.
2. Top-down: 1,800,000 / 200,000 = 9 orders.
3. Platform from bottom-up: 9 x 200,000 = 1.8 million.
**Result:** About 9 orders per restaurant per day (range 5-15); skewed, so the median is lower, around 5.
**Sanity check:** The two routes match, but I chose the inputs so they would; I would present the closeness as consistency, not proof.
**Sensitivity:** Delivery share of orders; at 15% the figure drops to 5.4.
**Likely follow-ups:** 1) *Why is the average above the median?* A few large restaurants take most orders. 2) *How would you check?* Use the platform's order table grouped by restaurant.
**Common mistakes / traps:** Treating the average as typical; ignoring the app's share; picking totals that make the cross-check true by construction.

### Q61 ⭐ 🟡 Estimate the revenue lost if a metro network is shut for one day.
**Asked at:** commonly asked (no company-specific report found); builds on the metro-riders guesstimate, unverified.
**What the interviewer is checking:** Whether you count every revenue stream and distinguish revenue lost from the wider city cost.
**Say this in the interview:** "Mainly fares: 5 million riders at about Rs 35 comes to Rs 17.5 crore, plus ads and other income, so roughly Rs 20 crore for the day."
**Clarify first:** A weekday, direct revenue to the metro company (fares, ads, rent), not the knock-on cost to the economy.
**Approach:** Revenue streams added up: fares, ads, other income.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Daily riders | 5 million | large network |
| Average fare | Rs 35 | mix of short and long trips |
| Annual ad revenue | Rs 140 crore | link to Q52 |
| Other income (property, parking, retail) | 10% of fares | assumed |
**Calculation:**
1. Fares = 5,000,000 x 35 = Rs 17.5 crore.
2. Ads = 140 crore / 365 = Rs 0.38 crore.
3. Other = 10% x 17.5 = Rs 1.75 crore.
4. Total = 17.5 + 0.38 + 1.75 = Rs 19.6 crore.
**Result:** About Rs 20 crore (range Rs 12-25 crore). On a Sunday with 3.5 million riders, fares are Rs 12.25 crore.
**Sanity check:** Annual = 19.6 x 365 = Rs 7,150 crore, high versus a typical large network's real revenue, so my fare and rider inputs may be generous; I would trim to the lower half of the range.
**Sensitivity:** Riders and fare multiply; a 20% lower fare gives Rs 3.5 crore less.
**Likely follow-ups:** 1) *Are costs saved?* Some (power, consumables), but staff and fixed costs remain. 2) *Is revenue recovered later?* Mostly not; trips are lost or shifted to buses and cabs.
**Common mistakes / traps:** Counting only fares; mixing revenue with the economic cost to the city; ignoring weekday versus weekend.

### Q62 ⭐ 🟡 Estimate the number of EV charging sessions a public charging station network completes in a day.
**Asked at:** commonly asked (no company-specific report found); a niche estimation prompt, unverified.
**What the interviewer is checking:** Whether you size by chargers times sessions each (utilisation) and separate fast from slow chargers.
**Say this in the interview:** "A network of 3,000 public chargers, split into fast and slow, with sessions per charger set by utilisation, gives about 10,000 sessions a day."
**Clarify first:** Public chargers only (not home), a network of about 3,000 charge points, an average day.
**Approach:** Bottom-up by charger type; check with utilisation and energy.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| DC fast chargers | 800 | highway and city hubs |
| Sessions per fast charger per day | 8 | session about 36 minutes |
| AC slow chargers | 2,200 | malls, offices |
| Sessions per AC charger per day | 1.5 | session about 3 hours |
**Calculation:**
1. Fast = 800 x 8 = 6,400 sessions.
2. Slow = 2,200 x 1.5 = 3,300 sessions.
3. Total = 9,700.
**Result:** About 10,000 sessions a day (range 5,000-15,000).
**Sanity check:** Utilisation: fast 8 x 0.6 h = 4.8 h of 24 = 20%; slow 1.5 x 3 h = 4.5 h = 19%. Energy: 6,400 x 25 kWh + 3,300 x 12 kWh = about 200 MWh a day, reasonable.
**Sensitivity:** Utilisation. If it is 10% instead of 20%, sessions halve to about 4,850.
**Likely follow-ups:** 1) *Peak hours?* Evening for slow, midday for highway fast chargers. 2) *Why low utilisation?* Few EVs per charger today.
**Common mistakes / traps:** Assuming 24-hour use; treating all chargers alike; counting home charging.

### Q63 ⭐ 🟡 A rider fleet manager says absenteeism is 8%, weekly off is 1 day in 7 and the peak needs 40 riders on duty. How many riders must be on the payroll?
**Given:** peak need 40 on duty; 6 of 7 days worked; 8% absenteeism on scheduled days. Round up.
**Asked at:** commonly asked (no company-specific report found); a roster-planning calculation (gap-fill, unverified). It resembles HR workforce-planning maths.
**What the interviewer is checking:** Whether you gross up in the right order: absenteeism first, weekly off second, then round up.
**Say this in the interview:** "To get 40 present with 8% absent I must schedule 43.5. Each rider is scheduled 6 of 7 days, so payroll is 43.5 x 7/6 = 50.7, which rounds up to 51."
**Definition in plain words:** Absenteeism is the share of scheduled people who do not show up. Payroll headcount = on-duty need / (1 - absenteeism) x 7/6.
**Worked answer:**
1. Present share = 1 - 0.08 = 0.92, so scheduled per day = 40 / 0.92 = 43.48.
2. Each rider is scheduled 6 of 7 days (6/7 = 0.857), so payroll = 43.48 / (6/7) = 43.48 x 7/6 = 50.72.
3. Round up to 51.
**Result:** 51 riders on the payroll.
**Check:** 51 x 6/7 = 43.7 scheduled; x 0.92 = 40.2 present, so 40 is covered. With 50 riders: 42.9 x 0.92 = 39.4, which is short.
**Caveats:** Assumes the weekly off is spread evenly across all days and that absence is spread evenly; real rosters also cover leave, training and seasonal peaks.
**Likely follow-ups:** 1) *If absenteeism is 12%?* 40 / 0.88 x 7/6 = 53.0, so 54 by rounding up (53.03). 2) *Does the shortcut 40 x 1.08 x 7/6 work?* It gives 50.4, also 51 here, but is theoretically wrong because 8% is a share of scheduled people, not of the need.
**Common mistakes / traps:** Adding 8% to 40; applying the weekly off backwards (x 6/7); rounding down.

### Q64 ⭐ 🟡 Estimate the cloud-kitchen output (meals per day) of a kitchen with 6 cooking stations.
**Asked at:** commonly asked (no company-specific report found); a capacity guesstimate, unverified.
**What the interviewer is checking:** Whether you distinguish maximum capacity from realistic output by using utilisation in peak and off-peak hours.
**Say this in the interview:** "Each station can do about 12 meals an hour, but only at peak. With peak and off-peak utilisation I get about 400 meals a day against a ceiling of 860."
**Clarify first:** Meals means individual dishes dispatched, one kitchen, open 12 hours (11 am to 11 pm), delivery only.
**Approach:** Capacity first, then utilisation by period.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Meals per station per hour at full speed | 12 | about 5 minutes per meal |
| Operating hours | 12 | 4 peak, 8 off-peak |
| Peak utilisation | 80% | lunch and dinner |
| Off-peak utilisation | 30% | |
**Calculation:**
1. Peak per station = 4 x 12 x 0.8 = 38.4 meals.
2. Off-peak per station = 8 x 12 x 0.3 = 28.8 meals.
3. Per station per day = 67.2.
4. Kitchen = 67.2 x 6 = 403 meals.
**Result:** About 400 meals a day (range 300-600).
**Sanity check:** Maximum capacity = 12 x 12 x 6 = 864 meals, so I assumed 47% overall utilisation, a believable figure for cloud kitchens.
**Sensitivity:** Peak utilisation. At 95% it rises to about 450; at 60%, about 360.
**Likely follow-ups:** 1) *How to raise output?* Prep ahead, shared stations, shorter menus. 2) *Meals versus orders?* An order often has 1.5-2 items.
**Common mistakes / traps:** Assuming full speed all day; mixing orders with items; ignoring prep and cleaning time.

### Q65 ⭐ 🟡 Estimate the number of fuel litres a city's food delivery fleet consumes in a day.
**Asked at:** commonly asked (no company-specific report found); a niche estimation, unverified.
**What the interviewer is checking:** Whether you chain riders, kilometres, mileage and the petrol share of the fleet.
**Say this in the interview:** "Riders times km per day, divided by mileage, only for petrol bikes. With 40,000 riders that is about 60,000 litres a day."
**Clarify first:** One large metro, active riders in a day, petrol two-wheelers only (EVs excluded).
**Approach:** Bottom-up chain; cross-check using orders.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Active riders in the city | 40,000 | large metro |
| Petrol share | 85% | rest EV or cycle |
| Distance per rider per day | 80 km | includes repositioning |
| Mileage | 45 km per litre | scooter or bike |
| Petrol price | Rs 100 per litre | assumed |
**Calculation:**
1. Petrol riders = 40,000 x 0.85 = 34,000.
2. Total km = 34,000 x 80 = 2.72 million km.
3. Litres = 2,720,000 / 45 = 60,400.
4. Cost = 60,400 x 100 = Rs 60 lakh a day.
**Result:** About 60,000 litres a day (range 35,000-90,000), around Rs 60 lakh.
**Sanity check:** Per order: if each rider does 12 orders, 80 km is 6.7 km per order, a bit high; with 60 km it would be about 45,000 litres, so I would put the range lower bound there.
**Sensitivity:** Distance per rider; every 10 km changes litres by about 7,500.
**Likely follow-ups:** 1) *Cost per order?* If each rider does 12 orders, that is 40,000 x 12 = 480,000 orders, so Rs 60 lakh / 480,000 = about Rs 12.5 of fuel per order. 2) *Effect of EV shift?* Each 10 points of EV share cuts about 7,000 litres.
**Common mistakes / traps:** Using car mileage; counting all registered riders; forgetting dead mileage while waiting or returning.

### Q66 ⭐ 🟡 Estimate the number of new rider onboardings a delivery platform needs per month to keep its fleet stable at 100,000 riders if monthly rider churn is 6%.
**Given:** fleet target 100,000; 6% of riders leave each month; no growth.
**Asked at:** commonly asked (no company-specific report found); a churn-replacement calculation, similar to attrition planning in HR (gap-fill, unverified).
**What the interviewer is checking:** Whether you see that stability means hires equal leavers each month.
**Say this in the interview:** "Churn of 6% of 100,000 is 6,000 leavers a month, so 6,000 new riders a month, which is 72,000 a year."
**Definition in plain words:** Monthly churn is the share of the fleet that leaves in a month. Replacement onboardings = fleet x churn.
**Worked answer:**
1. Leavers per month = 100,000 x 0.06 = 6,000.
2. For no growth, onboardings = leavers = 6,000.
3. Per year = 72,000, i.e. 72% of the fleet is replaced every year.
**Result:** 6,000 new riders a month.
**Check:** Start 100,000, minus 6,000, plus 6,000 = 100,000.
**Caveats:** If only 40% of signed-up applicants complete onboarding, you must attract 6,000 / 0.4 = 15,000 sign-ups a month. New riders usually quit faster than veterans, so true replacement needs may be higher. Churn is the same idea as HR attrition.
**Likely follow-ups:** 1) *To grow 5% a month?* Net +5,000, so 11,000 onboardings. 2) *Cut churn to 4%?* Needs 4,000.
**Common mistakes / traps:** Using the annual rate; forgetting the funnel drop-off; ignoring growth targets.

### Q67 ⭐ 🟡 A SaaS company has 800 customers paying ₹50,000 a month on average and loses 2% of customers every month with no new sales. What is its monthly revenue after 6 months?
**Given:** 800 customers; ₹50,000/month each; 2% monthly customer loss, compounded; no new customers or price change.
**Asked at:** commonly asked (no company-specific report found); a compounding-churn calculation (gap-fill, unverified).
**What the interviewer is checking:** Whether you compound the loss instead of subtracting 2% six times from the starting number.
**Say this in the interview:** "Each month keeps 98%. After 6 months I keep 0.98 to the power 6, about 88.6%, so about 709 customers and Rs 3.54 crore a month, down from Rs 4 crore."
**Definition in plain words:** Customer churn is the share of customers lost in a month. Customers after n months = start x (1 - churn)^n.
**Worked answer:**
1. Starting revenue = 800 x 50,000 = Rs 4 crore a month.
2. Retention after 6 months = 0.98^6 = 0.8858.
3. Customers = 800 x 0.8858 = 708.7, about 709.
4. Revenue = 708.7 x 50,000 = Rs 3.54 crore a month.
**Result:** About 709 customers and Rs 3.54 crore a month, a fall of Rs 0.46 crore (11.4%).
**Check:** Simple 12% off (6 x 2%) would give 704 customers; compounding loses fewer because each month's 2% applies to a smaller base.
**Caveats:** Customers are whole numbers (709 rounded); "after 6 months" means after six monthly losses; real SaaS churn varies by customer size.
**Likely follow-ups:** 1) *After 12 months?* 0.98^12 = 0.785, about 628 customers. 2) *Monthly revenue churn vs customer churn?* Differ if bigger customers leave less.
**Common mistakes / traps:** Subtracting 12% flat; using 0.98 x 6; compounding in the wrong direction.

### Q68 ⭐ 🟡 Estimate the number of orders placed on a food delivery app in a Tier-2 city of 1 million people on a weekday.
**Asked at:** prep sites list a PhonePe Bengaluru Sunday food-order guesstimate (candidate-style, unverified); this Tier-2 weekday version is a gap-fill.
**What the interviewer is checking:** Whether you adjust national or metro habits down for a smaller city and cross-check with restaurants.
**Say this in the interview:** "Population to adults to app users to orders per month, then divide by 30 and trim for a weekday. I get roughly 9,000 orders a day across all food apps."
**Clarify first:** All food delivery apps combined, a weekday (lower than weekend), orders not items.
**Approach:** Top-down from population; bottom-up cross-check from restaurants.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 1,000,000 | given |
| Adults | 70% | |
| Adults using a food app monthly | 12% | lower than metros |
| Orders per active user per month | 3.5 | |
| Weekday factor | 0.9 | vs average day |
**Calculation:**
1. Adults = 700,000; app users = 700,000 x 0.12 = 84,000.
2. Orders per month = 84,000 x 3.5 = 294,000.
3. Per average day = 294,000 / 30 = 9,800.
4. Weekday = 9,800 x 0.9 = 8,820.
**Result:** About 9,000 orders (range 4,000-15,000).
**Sanity check:** Restaurants: 1,500 on apps x 6 orders each = 9,000.
**Sensitivity:** Share of adults using the app; at 8% orders fall to about 5,900.
**Likely follow-ups:** 1) *Weekend?* Perhaps 1.2x, so about 11,800. 2) *Dinner peak?* About 45% of orders in 7-10 pm.
**Common mistakes / traps:** Using metro rates; forgetting not everyone is an adult; no cross-check.

### Q69 ⭐ 🔴 Estimate the warehouse floor area required for a fulfilment centre that ships 50,000 orders a day.
**Asked at:** commonly asked (no company-specific report found); a niche estimation, unverified.
**What the interviewer is checking:** Whether you size inventory in units, convert to volume, then to floor area, and add the non-storage space.
**Say this in the interview:** "50,000 orders times 2 items, 20 days of stock, converted to volume and floor space, plus working zones: roughly 3 lakh square feet."
**Clarify first:** General merchandise e-commerce (not groceries), stock cover of about 20 days, racked storage.
**Approach:** Inventory-driven bottom-up; cross-check with orders per square foot.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Items per order | 2 | |
| Days of stock | 20 | |
| Volume per unit | 0.01 m3 (10 litres) | average with packaging |
| Racking height | 5 m | |
| Space utilisation | 30% | aisles, gaps in racks |
| Storage share of total area | 50% | rest: receiving, packing, sorting, dispatch |
**Calculation:**
1. Units shipped a day = 50,000 x 2 = 100,000; stock = 100,000 x 20 = 2 million units.
2. Volume = 2,000,000 x 0.01 = 20,000 m3.
3. Effective height = 5 x 0.3 = 1.5 m, so storage floor = 20,000 / 1.5 = 13,333 m2.
4. Total area = 13,333 / 0.5 = 26,700 m2, which is 26,700 x 10.76 = about 287,000 sq ft.
**Result:** About 27,000 m2, roughly 3 lakh sq ft (range 1.5-4.5 lakh).
**Sanity check:** 50,000 orders / 287,000 sq ft = 0.17 orders per sq ft a day; I would say plausible for a mixed-goods centre, unverified.
**Sensitivity:** Days of stock; 10 days halves storage, so area falls to about 15,000 m2.
**Likely follow-ups:** 1) *Peak sale?* Size for peak or use temporary space. 2) *Automation?* Raises utilisation and cuts area.
**Common mistakes / traps:** Ignoring aisles and working zones; using daily orders only; mixing m2 and sq ft.

### Q70 ⭐ 🔴 Estimate the total payroll cost for the data and analytics team a food delivery company would need at 2 million orders a day, and state your headcount ratio assumptions.
**Asked at:** commonly asked (no company-specific report found); a niche estimation, unverified.
**What the interviewer is checking:** Whether you size by role, state ratios openly and convert to a total cost.
**Say this in the interview:** "I build the team by role: about 180 people, which is 1 data person per 11,000 daily orders, at an average Rs 21 lakh. Payroll is about Rs 37 crore a year, or Rs 45 crore with on-costs."
**Clarify first:** Annual cost-to-company (CTC) for permanent staff in India, not contractors; analytics includes data science and engineering.
**Approach:** Headcount by role, multiplied by assumed salaries.
**Assumptions (all assumed / approximate, unverified):**
| Role | Headcount | CTC (Rs lakh/year) |
|---|---|---|
| Business/data analysts | 70 | 10 |
| Data scientists | 40 | 28 |
| Data engineers | 35 | 24 |
| BI/dashboard developers | 15 | 12 |
| Managers and leads | 20 | 45 |
**Calculation:**
1. Headcount = 70 + 40 + 35 + 15 + 20 = 180.
2. Cost: 700 + 1,120 + 840 + 180 + 900 = Rs 3,740 lakh = Rs 37.4 crore.
3. Average = 37.4 crore / 180 = Rs 20.8 lakh.
4. With 20% on-costs (bonus, benefits, tools): Rs 44.9 crore.
**Result:** 180 people; Rs 37 crore a year payroll (Rs 45 crore loaded); range Rs 25-60 crore.
**Sanity check:** Ratio 2,000,000 / 180 = 1 data person per 11,000 daily orders; cost per order = 3,740 lakh / 730 million orders a year = about 51 paise.
**Sensitivity:** Headcount drives it; 150 people lowers cost to Rs 31 crore. Data scientist pay is the next biggest swing.
**Likely follow-ups:** 1) *Why this mix?* More analysts than scientists because most questions are descriptive. 2) *Ratio to company size?* Analytics at about 4-5% of corporate staff.
**Common mistakes / traps:** Forgetting managers; ignoring on-costs; using monthly salaries as annual.

### Q71 ⭐ 🔴 Estimate the number of UPI QR-code merchants a payments app must onboard to reach a stated daily transaction target of 50 million transactions.
**Asked at:** commonly asked (no company-specific report found); a niche estimation, unverified.
**What the interviewer is checking:** Whether you separate onboarded from active merchants and apply a realistic transactions per merchant.
**Say this in the interview:** "Merchant payments are about 75% of the target; each active merchant does about 12 a day, and 60% of onboarded merchants are active. That gives about 5.2 million merchants."
**Clarify first:** The target counts all transactions, of which merchant payments (scans of a QR code) are one part; the rest are person-to-person.
**Approach:** Top-down from the target to active merchants, then to onboarded merchants.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Target transactions | 50 million a day | given |
| Share from merchant QR payments | 75% | rest are person-to-person |
| Transactions per active merchant per day | 12 | mix of small shops and larger stores |
| Active share of onboarded merchants | 60% | many QR codes sit unused |
**Calculation:**
1. Merchant transactions = 50,000,000 x 0.75 = 37.5 million.
2. Active merchants = 37,500,000 / 12 = 3.125 million.
3. Onboarded merchants = 3,125,000 / 0.6 = 5.21 million.
**Result:** About 5.2 million merchants (range 3-8 million).
**Sanity check:** 50 million / 5.2 million = about 9.6 transactions per onboarded merchant per day, plausible for small shops.
**Sensitivity:** Transactions per merchant; at 20 a day the answer drops to about 3.1 million, and at 8 it rises to 7.8 million.
**Likely follow-ups:** 1) *Which merchants first?* Higher-frequency ones (tea stalls, grocers). 2) *Market share?* Competing apps share the same QR codes, so onboarding does not guarantee transactions.
**Common mistakes / traps:** Counting all onboarded as active; ignoring person-to-person; assuming one QR code equals one merchant.

### Q72 ⭐ 🔴 Estimate the daily wastage cost in a quick-commerce dark store for fresh produce, and how you would validate it.
**Asked at:** commonly asked (no company-specific report found); a niche estimation, unverified.
**What the interviewer is checking:** Whether you estimate wastage as a percentage of produce sales at cost and name concrete ways to check it.
**Say this in the interview:** "Store sales, times the fresh produce share, times a 4% wastage rate, at cost, gives about Rs 2,500 a day per store. I would validate it against stock records and spoilage logs."
**Clarify first:** One dark store, fruit and vegetables only, wastage valued at cost price, a normal day.
**Approach:** Top-down percentage; validate bottom-up from stock-in, stock-out and write-off logs.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Orders per day | 1,200 | busy store |
| Average order value | Rs 550 | |
| Fresh produce share of sales | 12% | |
| Wastage rate on produce sales | 4% | assumed range 2-8% |
| Cost as share of sales price | 80% | |
**Calculation:**
1. Store sales = 1,200 x 550 = Rs 660,000.
2. Produce sales = 12% x 660,000 = Rs 79,200.
3. Wastage at sales value = 4% x 79,200 = Rs 3,168.
4. At cost = 3,168 x 0.8 = Rs 2,534.
**Result:** About Rs 2,500 a day per store (range Rs 1,300-5,100 for 2-8% wastage), about Rs 76,000 a month.
**Sanity check:** Per order that is Rs 2.1 of wastage, small but meaningful against thin margins.
**Validation:** (1) Stock reconciliation: opening stock plus received minus sold minus closing stock should equal wastage. (2) Daily write-off log with reason (spoiled, damaged, trimmed). (3) Weigh-in a sample week. (4) Compare stores with similar volumes.
**Sensitivity:** Wastage rate. At 8% the cost doubles to about Rs 5,070.
**Likely follow-ups:** 1) *How to reduce it?* Better demand forecasts, smaller batches, markdowns near expiry. 2) *Do you count unsold items given away?* Yes, as loss.
**Common mistakes / traps:** Valuing at selling price instead of cost; ignoring shrink from theft or miscounts; no validation plan.


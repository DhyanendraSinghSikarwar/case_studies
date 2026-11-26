# Book 10 — Domain Knowledge | Part 6: Marketing & Sales Analytics 🟢🟡🔴

**Target:** 80 questions | **Actual:** 93 questions
**Scope:** marketing and sales analytics vocabulary, funnel and campaign metrics, attribution, CRM and pipeline data, segmentation, pricing and promotions, data sources, consent and privacy awareness, and domain case questions (generic metric definitions are in Book 7 Part 4).

### Q1 ⭐⭐⭐ 🟢 What is the marketing funnel (awareness, consideration, conversion, retention), and which metric would you track at each stage?
**Asked at:** commonly asked (no company-specific report found); funnel questions appear in marketing analyst prep guides (prep-site guides, unverified).
**What the interviewer is checking:** Whether you can link each stage of a customer's journey to a number you would actually measure.
**Say this in the interview:** "The funnel is the path from a stranger to a loyal customer: awareness, consideration, conversion, retention. I track reach and impressions at the top, clicks and leads in the middle, orders and cost per customer at conversion, and repeat purchase rate after that."
**Explain simply:**
- **Awareness:** people first hear of us. Metrics: *impressions* (times an ad was shown), *reach* (distinct people who saw it), website visits.
- **Consideration:** people compare us with others. Metrics: click-through rate, leads (people who left contact details), time on site, demo or trial requests.
- **Conversion:** people buy. Metrics: conversion rate, number of new customers, cost per acquisition (marketing spend divided by new customers).
- **Retention:** people come back. Metrics: repeat purchase rate, churn (share of customers who leave), customer lifetime value.
- The funnel narrows: far fewer people buy than see an ad. The analyst's job is to find the stage where the biggest share drops out.
- **HR parallel:** the hiring funnel (applications, screened, interviewed, offered, joined, retained at one year) has the same shape.
**Likely follow-ups:** 1) *Is the funnel really linear?* No; people skip stages or loop back, so treat it as a simplification. 2) *Which stage matters most?* The one with the biggest fixable leak, often retention because keeping a customer is cheaper than finding a new one.
**Common mistakes:** Naming only top-of-funnel vanity metrics; forgetting retention; assuming stage names and metric definitions are identical across companies.

### Q2 ⭐⭐⭐ 🟢 What is the difference between a marketing qualified lead (MQL) and a sales qualified lead (SQL), and who decides when a lead moves from one to the other?
**Asked at:** commonly asked (no company-specific report found); MQL/SQL definitions appear in vendor KPI pages and sales analyst guides (unverified).
**What the interviewer is checking:** That you know marketing and sales hand leads to each other and that the handover rule is agreed, not automatic.
**Say this in the interview:** "An MQL is a lead marketing thinks is worth passing on, based on interest such as downloading a guide. An SQL is a lead sales has checked and accepted as a real buying opportunity. Marketing usually flags the MQL by a scoring rule; sales decides the SQL after speaking to the person."
**Explain simply:**
- **Lead:** a person or company that has shown interest and left contact details.
- **MQL (marketing qualified lead):** fits the target profile and has shown enough engagement (visited pricing page, opened emails). Marketing's judgement, often an automatic score threshold.
- **SQL (sales qualified lead):** a sales rep has had a conversation and confirmed need, budget and timing (the exact checklist varies by company).
- **Who decides:** the two teams agree the rules in a *service level agreement* (SLA), a written promise such as "sales follows up within 24 hours". Sales accepts or rejects each MQL with a reason.
- **Why analysts care:** the MQL-to-SQL rate shows whether marketing and sales agree on what a "good" lead is.
**Likely follow-ups:** 1) *What if sales rejects most MQLs?* Review the scoring rules and the reject reasons with both teams. 2) *Is there a stage after SQL?* Yes, an opportunity (see Q7).
**Common mistakes:** Treating MQL and SQL as universal definitions; counting MQLs as sales success; ignoring how fast sales followed up.

### Q3 ⭐⭐⭐ 🟢 What do CTR, CPC, CPM and CPL stand for, and how is each calculated?
**Asked at:** commonly asked (no company-specific report found); ad-metric formulas are standard in marketing analyst guides (unverified as real company questions).
**What the interviewer is checking:** That you know the formulas and the denominators.
**Say this in the interview:** "CTR is click-through rate: clicks divided by impressions. CPC is cost per click: spend divided by clicks. CPM is cost per thousand impressions: spend divided by impressions times 1,000. CPL is cost per lead: spend divided by leads."
**Explain simply:**
- **Impression:** one showing of an ad on a screen. **Click:** someone tapping it. **Lead:** someone who gave contact details.
- **CTR = clicks / impressions** (a percentage). It tells you whether the ad is attractive.
- **CPC = spend / clicks.** The price of bringing one visitor.
- **CPM = spend / impressions x 1,000.** M is the Roman numeral for thousand. It is the price of reach, used by awareness campaigns.
- **CPL = spend / leads.** The price of one enquiry, but not all leads are equal (see Q41).
- Each metric covers one stage of the funnel (Q1); a cheap click is worthless if it never turns into a customer.
**Worked example:** see Q13 for all of these computed on one campaign.
**Likely follow-ups:** 1) *CPM or CPC for a brand campaign?* CPM, since the goal is being seen. 2) *Is a low CPL always good?* No, check lead quality.
**Common mistakes:** Forgetting the x 1,000 in CPM; dividing clicks by reach instead of impressions; comparing CPL across channels without checking quality.

### Q4 ⭐⭐⭐ 🟢 What is ROAS, how is it different from marketing ROI, and why can a high ROAS still lose money?
**Asked at:** commonly asked (no company-specific report found); the ROAS-looks-good-but-profit-is-poor theme is common in marketing analyst guides (prep-site guides, unverified).
**What the interviewer is checking:** Whether you separate revenue per ad rupee from actual profit.
**Say this in the interview:** "ROAS is return on ad spend: revenue from ads divided by ad spend. Marketing ROI is profit gained after costs, divided by cost. A high ROAS can still lose money if the product margin is thin, because revenue is not profit."
**Explain simply:**
- **ROAS = ad revenue / ad spend.** Spend Rs 1 lakh, earn Rs 3 lakh revenue: ROAS 3.0.
- **Marketing ROI = (profit attributable to marketing - marketing cost) / marketing cost.** Definitions vary (some vendors define it differently), so state yours.
- **Why high ROAS can lose money:** if the gross margin is 20%, Rs 3 of revenue gives only Rs 0.60 of gross profit per Rs 1 of ads, a loss. The break-even ROAS is 1 divided by the margin (see Q15).
- **Other traps:** revenue from customers who would have bought anyway (Q36), returns and cancellations not deducted, and costs such as discounts, delivery and team salaries left out.
**Likely follow-ups:** 1) *Which would you show leadership?* Both, plus margin-adjusted ROAS. 2) *Is ROAS 1 break-even?* Only if margin is 100%, which never happens.
**Common mistakes:** Treating ROAS and ROI as the same; ignoring margin; using gross revenue before returns.

### Q5 ⭐⭐⭐ 🟢 What is marketing attribution, and why is it hard to say which campaign caused a sale?
**Asked at:** commonly asked (no company-specific report found); attribution is a standard topic in marketing analytics guides (prep-site guides, unverified).
**What the interviewer is checking:** That you understand credit assignment is a modelling choice, not a fact.
**Say this in the interview:** "Attribution is deciding which marketing touches deserve credit for a sale. It is hard because a customer sees many ads across devices and offline channels, and we usually cannot prove which one changed their mind."
**Explain simply:**
- **Touchpoint:** any contact between customer and brand: an ad, an email, a store visit, a friend's recommendation.
- **The problem:** a buyer may see a video, search on Google, get an email, then buy. Who earned the sale? Every rule you pick gives a different answer.
- **Why it is hard:** people use several devices; tracking is limited by privacy rules and browser changes; offline influence (word of mouth, TV) is invisible; and some buyers would have bought anyway.
- **Correlation is not cause:** attribution shows which touches *appeared before* a sale, not which *caused* it. Causation needs experiments (Q36, Q39).
- **HR parallel:** which job portal "caused" a hire when the candidate saw the ad, got a referral and then applied?
**Likely follow-ups:** 1) *How do you check an attribution model?* Compare with a holdout test. 2) *What do you do in practice?* Use one agreed model consistently and say its limits.
**Common mistakes:** Presenting attribution as truth; mixing models between reports; trusting each platform's own numbers, which each claim credit for the same sale.

### Q6 ⭐⭐⭐ 🟢 What are first-touch, last-touch, linear, time-decay and position-based attribution models, and when does each mislead?
**Asked at:** commonly asked (no company-specific report found); the five standard models are listed in marketing analytics guides (prep-site guides, unverified).
**What the interviewer is checking:** That you can apply each rule and name its blind spot.
**Say this in the interview:** "First-touch gives all credit to the first contact, last-touch to the final one, linear splits equally, time-decay gives more to touches nearer the sale, and position-based typically gives most to first and last. Each misleads in a different way."
**Explain simply:**
- **First-touch:** all credit to the first interaction. Misleads by ignoring what closed the sale; flatters awareness channels.
- **Last-touch:** all credit to the final interaction. Misleads by favouring bottom-funnel channels such as branded search and email; this is often the default.
- **Linear:** equal share to every touch. Misleads because a casual banner view counts as much as a demo.
- **Time-decay:** more credit as the touch gets closer to the sale. Misleads on long B2B cycles where early touches did the heavy lifting.
- **Position-based (U-shaped):** a common split is 40% first, 40% last, 20% shared by the middle (the split is a choice, not a rule). Misleads because the weights are arbitrary.
- **Worked example:** see Q16.
**Likely follow-ups:** 1) *Which is best?* None; pick by sales-cycle length and question asked. 2) *Is there a data-driven option?* Yes, models that learn weights from many journeys, but they need lots of data.
**Common mistakes:** Saying one model is "correct"; not stating the weights used; comparing reports built on different models.

### Q7 ⭐⭐⭐ 🟢 In a CRM such as Salesforce or HubSpot, what are a lead, contact, account and opportunity, and how do they relate to each other?
**Asked at:** commonly asked (no company-specific report found); CRM object definitions are asked in sales and marketing analyst rounds (job postings and prep guides, unverified). Naming differs by tool; the description below is the common pattern.
**What the interviewer is checking:** That you know the main tables in a CRM and how they join.
**Say this in the interview:** "A lead is an unqualified person who showed interest. A contact is a known person at a company. An account is the company. An opportunity is a specific potential deal. One account has many contacts and can have many opportunities."
**Explain simply:**
- **CRM (customer relationship management):** software where sales and marketing record every customer interaction. Salesforce and HubSpot are examples.
- **Lead:** raw interest, not yet checked. When qualified, it is *converted*.
- **Account:** the organisation (in B2C tools sometimes the person).
- **Contact:** an individual linked to an account, such as the HR head of that company.
- **Opportunity (deal):** a possible sale with an amount, expected close date and stage.
- **Relationships:** lead converts into contact + account + opportunity; account 1-to-many contacts; account 1-to-many opportunities. HubSpot uses "company" and "deal" for account and opportunity.
**Likely follow-ups:** 1) *What is the key for joining?* Account ID on contacts and opportunities. 2) *What happens to the lead record after conversion?* Usually kept, flagged converted.
**Common mistakes:** Treating lead and contact as the same; counting contacts as customers; ignoring duplicate accounts.

### Q8 ⭐⭐⭐ 🟢 What is a sales pipeline, what are its typical stages, and what does an analyst measure about it?
**Asked at:** commonly asked (no company-specific report found); pipeline questions appear in sales analyst guides (prep-site guides, unverified).
**What the interviewer is checking:** That you know the stages and the numbers that show pipeline health.
**Say this in the interview:** "A pipeline is the set of open deals by stage, from first contact to closed. Typical stages are lead, qualified, proposal, negotiation, won or lost. I measure pipeline value, conversion between stages, how long deals sit in each stage, and coverage against target."
**Explain simply:**
- **Typical stages (names vary):** new lead, qualified, demo or proposal, negotiation, closed won, closed lost.
- **Pipeline value:** the total of open deal amounts. Sometimes *weighted* by the chance of winning at each stage.
- **Stage conversion:** the share of deals that move from one stage to the next (worked in Q14).
- **Stage ageing:** days a deal has been in its stage; old deals are often dead.
- **Coverage:** pipeline divided by target (Q40). **Velocity:** how fast value moves through (Q46).
- **Creation:** new pipeline added per week, as the leading indicator of future sales.
**Likely follow-ups:** 1) *What is a stalled deal?* One with no activity or stage change beyond a typical time. 2) *Why weighted pipeline?* Because a Rs 10 lakh early-stage deal is less likely than the same deal in negotiation.
**Common mistakes:** Summing all open deals as if they will close; ignoring stale deals; using different stage definitions by team.

### Q9 ⭐⭐⭐ 🟢 What are win rate, average deal size and sales cycle length, and why do sales leaders watch all three together?
**Asked at:** commonly asked (no company-specific report found); these three are standard sales analytics measures (prep-site guides, unverified).
**What the interviewer is checking:** That you see how the three combine into revenue speed.
**Say this in the interview:** "Win rate is the share of deals won, average deal size is revenue per won deal, and sales cycle length is days from opportunity creation to close. Leaders watch them together because improving one can hurt another, for example discounting raises win rate but shrinks deal size."
**Explain simply:**
- **Win rate = won deals / (won + lost deals)** for deals that closed in a period. Some firms divide by all created deals; state which.
- **Average deal size = total won value / number of won deals.**
- **Sales cycle length = average days from creation to close** (usually for won deals).
- **Together:** more revenue comes from a higher win rate, bigger deals, or faster cycles. Chasing small quick deals shortens the cycle but cuts size; chasing big deals lengthens it and lowers win rate.
- They are the inputs to pipeline velocity (Q46).
**Likely follow-ups:** 1) *Would you use mean or median deal size?* Median if a few huge deals skew the average. 2) *Is a rising win rate always good?* Not if reps stopped chasing hard deals.
**Common mistakes:** Including open deals in win rate; mixing definitions across teams; ignoring segment mix when comparing periods.

### Q10 ⭐⭐⭐ 🟢 What is customer segmentation, and why do marketing teams segment customers instead of treating everyone the same?
**Asked at:** commonly asked (no company-specific report found); segmentation is a staple of marketing analyst guides (prep-site guides, unverified).
**What the interviewer is checking:** That you can say why one message for all wastes money.
**Say this in the interview:** "Segmentation divides customers into groups that behave or need similar things, so each group gets a fitting offer. It raises response and cuts waste compared with treating everyone the same."
**Explain simply:**
- **Examples of bases:** who they are (age, city, company size), what they do (purchases, app usage), what they value (price or quality).
- **Why segment:** a heavy buyer needs a loyalty reward; a lapsed buyer needs a win-back nudge; discounting to someone who would pay full price loses margin.
- **How analysts do it:** rule-based groups (e.g. orders in last 90 days), RFM (Q11), or clustering (grouping similar customers by algorithm).
- **Good segments are:** distinct, big enough to act on, measurable and actionable.
- **HR parallel:** employee groups (new joiners, high performers, flight risks) get different engagement plans.
**Likely follow-ups:** 1) *How many segments?* As many as the team can act on, often 4 to 6. 2) *How do you test value?* Compare response and revenue between segment-targeted and generic campaigns.
**Common mistakes:** Creating segments nobody can act on; using personal data without consent; letting segments go stale.

### Q11 ⭐⭐⭐ 🟢 What is RFM analysis, and what business decisions does it support?
**Asked at:** commonly asked (no company-specific report found); RFM is a common segmentation topic (HubSpot and prep-site guides, unverified).
**What the interviewer is checking:** That you know the three measures and can link scores to actions.
**Say this in the interview:** "RFM scores each customer on Recency (how recently they bought), Frequency (how often) and Monetary value (how much they spent). It helps decide who gets loyalty rewards, who gets a win-back offer and who to stop spending on."
**Explain simply:**
- **R:** days since last purchase; lower is better.
- **F:** number of orders in a period; higher is better.
- **M:** total spend; higher is better.
- **Scoring:** rank customers and give each measure a score, say 1 to 5 or 1 to 3. High on all three is a *champion*; high F and M but poor R is *at risk*.
- **Decisions supported:** reward champions, win back at-risk customers, welcome new ones, cut spend on dormant low-value ones.
- **Worked example:** see Q43.
**Likely follow-ups:** 1) *What are RFM's limits?* It looks only at the past and ignores why people buy. 2) *How often to refresh?* Regularly, since recency changes daily.
**Common mistakes:** Fixed score cut-offs that do not suit the data; ignoring product mix; treating RFM as prediction.

### Q12 ⭐⭐⭐ 🟢 What are UTM parameters, and what goes wrong in campaign reporting when they are used inconsistently?
**Asked at:** commonly asked (no company-specific report found); UTM tagging appears in marketing analytics guides (prep-site guides, unverified).
**What the interviewer is checking:** That you know campaign tagging is where reporting quality starts.
**Say this in the interview:** "UTM parameters are tags added to a link's web address, such as source, medium and campaign, so analytics tools know which campaign sent each visitor. If they are used inconsistently, the same campaign splits into many names and the report cannot be trusted."
**Explain simply:**
- **Common tags:** utm_source (where, e.g. instagram), utm_medium (type, e.g. paid_social), utm_campaign (name), plus optional utm_content and utm_term.
- **What goes wrong:** "Facebook", "facebook" and "fb" appear as three sources; missing tags push traffic into "direct" or "unassigned"; tagged internal links overwrite the true source.
- **Effect:** channel totals are wrong, ROAS by channel is wrong, and budgets get moved on bad evidence.
- **Fixes:** a naming convention in a shared sheet, lowercase only, link builders, and a regular audit of "unassigned" traffic.
**Likely follow-ups:** 1) *Do UTMs track offline?* No; use coupon codes or QR links. 2) *How do you clean existing data?* Map variants to a standard list in a lookup table.
**Common mistakes:** Mixed case; tagging internal links; leaving out the medium.

### Q13 ⭐⭐⭐ 🟡 A campaign had the figures below. Calculate CTR, CPC, CPM, CPL, CPA (cost per customer) and ROAS.
Spend Rs 2,00,000; impressions 40,00,000; clicks 80,000; leads 2,400; new customers 120; revenue Rs 6,00,000.
**Asked at:** commonly asked (no company-specific report found); campaign-metric calculations are common in marketing analyst rounds (prep-site guides, unverified).
**What the interviewer is checking:** Correct formulas, units and a sensible reading of the results.
**Say this in the interview:** "CTR is 2%, CPC is Rs 2.50, CPM is Rs 50, CPL is about Rs 83, CPA is about Rs 1,667 and ROAS is 3.0."
**Explain simply:**
- Each metric divides spend or an outcome by a different stage count (see Q3).
**Worked example:** (all figures computed by code; rounded to 2 decimals; Rs 2,00,000 = 200,000)
- CTR = 80,000 / 4,000,000 = **2.0%**
- CPC = 200,000 / 80,000 = **Rs 2.50**
- CPM = 200,000 / 4,000,000 x 1,000 = **Rs 50**
- CPL = 200,000 / 2,400 = **Rs 83.33**
- CPA (cost per new customer) = 200,000 / 120 = **Rs 1,666.67**
- ROAS = 600,000 / 200,000 = **3.0**
- Reading: each customer brought Rs 5,000 revenue (600,000 / 120) for Rs 1,667 cost. Profit depends on margin (Q15). Lead-to-customer rate is 120 / 2,400 = 5%.
**Likely follow-ups:** 1) *Is ROAS 3 good?* Only against break-even ROAS for the product margin. 2) *Where is the weak stage?* Compare stage rates with past campaigns.
**Common mistakes:** CPM without x 1,000; using leads as the CPA denominator; stating ROAS as a percentage without saying so.

### Q14 ⭐⭐⭐ 🟡 Find the stage-wise conversion rates, the lead-to-won rate and the marketing cost per won deal from the funnel below.
Leads 5,000; MQLs 1,500; SQLs 600; opportunities 240; won 48. Marketing spend Rs 6,00,000.
**Asked at:** commonly asked (no company-specific report found); funnel conversion calculations are common in sales and marketing analyst rounds (prep-site guides, unverified).
**What the interviewer is checking:** That you divide each stage by the previous one and also report end-to-end.
**Say this in the interview:** "Stage rates are 30%, 40%, 40% and 20%. Lead-to-won is 0.96%, and marketing cost per won deal is Rs 12,500."
**Explain simply:**
- *MQL* = marketing qualified lead, *SQL* = sales qualified lead (Q2); an *opportunity* is a live potential deal (Q7).
- Stage rate = this stage / previous stage; end-to-end = last / first.
**Worked example:** (computed by code; percentages exact)
- Leads to MQL: 1,500 / 5,000 = **30%**
- MQL to SQL: 600 / 1,500 = **40%**
- SQL to opportunity: 240 / 600 = **40%**
- Opportunity to won: 48 / 240 = **20%**
- Lead to won: 48 / 5,000 = **0.96%** (also 0.3 x 0.4 x 0.4 x 0.2)
- Cost per won deal = 600,000 / 48 = **Rs 12,500**; cost per lead = Rs 120.
- Marketing cost only: sales salaries and discounts are not included, so full acquisition cost is higher.
- Biggest leak in percentage terms is the last stage (20%), but fixing it is a sales task; the largest absolute drop is the first (3,500 leads lost).
**Likely follow-ups:** 1) *Which stage to improve?* Where a small lift is cheapest and the owner can act; for example, lifting MQL-to-SQL from 40% to 45% adds deals without extra ad spend. 2) *Is the cost per won deal fair?* Compare with deal value.
**Common mistakes:** Dividing every stage by total leads then calling it stage conversion; mixing percentage and percentage points; ignoring time lag between stages.

### Q15 ⭐⭐⭐ 🟡 A channel shows ROAS of 4.0 and the product has a gross margin of 30%. Is the channel profitable, and what is the break-even ROAS?
**Asked at:** commonly asked (no company-specific report found); break-even ROAS is a common margin-aware follow-up to ROAS questions (prep-site guides, unverified).
**What the interviewer is checking:** That you convert revenue return into profit using margin.
**Say this in the interview:** "Break-even ROAS is 1 divided by the gross margin, so 1 / 0.30 = 3.33. At ROAS 4.0 the channel earns Rs 1.20 gross profit per Rs 1 of ads, a Rs 0.20 gain, so it is profitable on gross margin, but only just."
**Explain simply:**
- *Gross margin* = (price minus product cost) / price; here 30%.
- Per Rs 1 of ad spend, revenue is Rs 4 and gross profit is 4 x 0.30.
**Worked example:** (computed by code)
- Gross profit per Rs 1 spend = 4.0 x 0.30 = Rs 1.20
- Net after ad cost = 1.20 - 1.00 = **Rs 0.20 per Re 1**, a 20% return on ad spend
- Break-even ROAS = 1 / 0.30 = **3.33**; ROAS 4.0 is 0.67 above it
- For Rs 1,00,000 spend: revenue Rs 4,00,000, gross profit Rs 1,20,000, net Rs 20,000.
- Caveat: other costs (delivery, returns, discounts, platform fees) are not counted; if they take more than 5 points of margin (30% minus the 25% break-even margin, which is 1 / 4, at ROAS 4), the channel loses money.
**Likely follow-ups:** 1) *What if margin is 20%?* Break-even ROAS 5; ROAS 4 would lose. 2) *Does new vs repeat matter?* Yes (Q19).
**Common mistakes:** Calling ROAS 4 profitable without margin; confusing margin with markup; leaving out returns.

### Q16 ⭐⭐⭐ 🟡 A customer clicked a Google ad, then an Instagram ad, then an email, and bought for Rs 10,000. Split the credit across the three touches under first-touch, last-touch and linear attribution.
**Asked at:** commonly asked (no company-specific report found); attribution split calculations are common in marketing analyst guides (prep-site guides, unverified).
**What the interviewer is checking:** Correct application of each rule and awareness that the choice changes channel credit.
**Say this in the interview:** "First-touch gives Google Rs 10,000; last-touch gives email Rs 10,000; linear gives each Rs 3,333.33."
**Explain simply:**
- Touches in order: Google ad, Instagram ad, email. Same sale, three different stories.
**Worked example:** (computed by code; linear rounded to 2 decimals)
| Model | Google ad | Instagram ad | Email |
|---|---|---|---|
| First-touch | Rs 10,000 | Rs 0 | Rs 0 |
| Last-touch | Rs 0 | Rs 0 | Rs 10,000 |
| Linear | Rs 3,333.33 | Rs 3,333.33 | Rs 3,333.33 |
- Each row sums to the total Rs 10,000 under each model (linear: 3,333.33 x 3 = 9,999.99, rounding gap of Re 0.01).
- Instagram gets nothing under first or last touch, though it may have helped.
**Likely follow-ups:** 1) *Position-based split here?* With 40/40/20 it is Rs 4,000 / Rs 2,000 / Rs 4,000 (weights are a choice, see Q6). 2) *Which would you report?* One agreed model, plus a note on its bias.
**Common mistakes:** Credits that do not add to the sale total; mixing models across channels; assuming the email "caused" the sale because it came last.

### Q17 ⭐⭐⭐ 🟡 A 10% discount cuts the unit margin from 30% to 20% of the original price. How much must volume rise for gross profit to stay the same, and what does that tell you about discount planning?
Original price Rs 100, unit cost Rs 70, baseline sales 1,000 units.
**Asked at:** commonly asked (no company-specific report found); discount break-even maths appears in pricing and promotion guides (unverified).
**What the interviewer is checking:** Whether you know a discount comes straight out of margin, so volume must rise by far more than the discount.
**Say this in the interview:** "Profit per unit falls from Rs 30 to Rs 20, so I need 1,500 units to earn the same Rs 30,000. That is a 50% volume rise to pay for a 10% discount."
**Explain simply:**
- **Gross profit** is selling price minus the direct cost of the product, times units sold.
- The cost stays Rs 70 whatever the price, so the whole Rs 10 discount comes out of the Rs 30 margin: a one-third cut in profit per unit.
- To earn the same total with a third less per unit, you must sell half as much again (30 / 20 = 1.5).
- The thinner the margin, the worse it gets. This is why discounts on low-margin items are risky.
**Worked example:** (all figures computed)
- Before: (100 - 70) x 1,000 = Rs 30,000.
- After discount: price Rs 90, margin Rs 20 per unit (20% of the original Rs 100, or 22.2% of the new Rs 90).
- Break-even units = 30,000 / 20 = 1,500, so volume must rise by 500 units, which is **50%** (a 10% price cut needs a 50% volume rise).
- Formula: required volume rise = discount / (old margin - discount), here 10 / (30 - 10) = 50%.
**Likely follow-ups:** 1) *What if the margin were 50%?* Required rise = 10 / 40 = 25%. 2) *What else must be true?* The extra volume must be new demand, not customers who would have bought anyway or who bought early.
**Common mistakes:** Assuming a 10% discount needs only a 10% volume rise; quoting margin as a percentage of the new price without saying so; ignoring that the Rs 10 comes off profit, not off revenue.

### Q18 ⭐⭐⭐ 🟡 A promotion lifted daily sales as below. Calculate the incremental units, the incremental gross profit and say whether the promotion paid off.
Baseline 1,000 units/day at Rs 100 price and Rs 70 cost. During a 7-day promotion at Rs 90, sales were 1,500 units/day. Ignore post-promotion dips.
**Asked at:** commonly asked (no company-specific report found); uplift versus baseline is a staple of retail promotion guides (unverified).
**What the interviewer is checking:** Whether you judge a promotion on profit against a baseline, not on the sales spike.
**Say this in the interview:** "Incremental units are 3,500 and revenue is up, but gross profit is Rs 2,10,000 either way, so the promotion only breaks even before its other costs. I would not call it a success."
**Explain simply:**
- **Baseline** means what would have sold without the promotion (here given as 1,000 a day).
- **Incremental** means the extra over that baseline.
- Sales jumped 50% and revenue rose 35%, which looks great, but each unit now earns Rs 20 instead of Rs 30.
- Any extra cost (ads, printing, handling) or lost sales from other products makes it a loss.
**Worked example:** (computed; 7 days)
- Incremental units = (1,500 - 1,000) x 7 = **3,500**.
- Baseline revenue = 100 x 1,000 x 7 = Rs 7,00,000; promo revenue = 90 x 1,500 x 7 = Rs 9,45,000, so revenue is up Rs 2,45,000.
- Baseline gross profit = 30 x 1,000 x 7 = Rs 2,10,000; promo gross profit = 20 x 1,500 x 7 = Rs 2,10,000.
- **Incremental gross profit = Rs 0.** It matches Q17: a 50% lift exactly offsets this discount.
**Likely follow-ups:** 1) *What would make it pay off?* A lift above 1,500 a day, or a lower discount. 2) *What would you also check?* Cannibalisation (shoppers switching from other products), stock-piling, and the post-promotion dip, which we were told to ignore.
**Common mistakes:** Celebrating revenue or unit growth; forgetting the discounted units that would have sold anyway at full price; leaving out campaign costs.

### Q19 ⭐⭐⭐ 🟡 Last month's paid campaign spent Rs 1,00,000 and reported Rs 4,00,000 revenue, but half of that revenue came from customers who had bought before. What are the blended ROAS and the new-customer ROAS, and which would you report?
**Asked at:** commonly asked (no company-specific report found); new versus returning split is a standard follow-up in marketing analyst guides (unverified).
**What the interviewer is checking:** Whether you question what the headline ROAS includes.
**Say this in the interview:** "Blended ROAS is 4.0 and new-customer ROAS is 2.0. I would report both, and lead with new-customer ROAS if the campaign's goal was acquisition."
**Explain simply:**
- **ROAS** (return on ad spend) is revenue from the ads divided by ad spend.
- **Blended** here means all customers together; **new-customer** counts only first-time buyers.
- Repeat customers may have bought anyway, so the ad may deserve little of that credit. New-customer revenue is the safer view of growth.
- Neither is profit: compare with gross margin (see break-even ROAS).
**Worked example:** (computed)
- Blended ROAS = 4,00,000 / 1,00,000 = **4.0**.
- New-customer revenue = 4,00,000 x 50% = Rs 2,00,000, so new-customer ROAS = 2,00,000 / 1,00,000 = **2.0**.
- The headline is cut in half once repeat buyers are removed.
**Likely follow-ups:** 1) *Is new-customer ROAS the true value?* No; a new customer may buy again, so compare with lifetime value. 2) *Is repeat revenue worthless?* Not always; the ad may have triggered the purchase, which only an incrementality test shows.
**Common mistakes:** Reporting only the flattering 4.0; treating all attributed revenue as caused by the ad; ignoring margin.

### Q20 ⭐⭐⭐ 🟡 What data and tables would you need to build a campaign performance report, and what first cuts would you produce?
**Asked at:** commonly asked (no company-specific report found); campaign reporting is the core task in marketing analyst guides and job postings (unverified).
**What the interviewer is checking:** Whether you can link spend, clicks, leads and revenue into one view.
**Say this in the interview:** "I need spend and clicks from the ad platforms, leads and sales from the CRM, and a campaign key such as UTM tags to join them. First I would show cost, leads, customers and revenue by campaign and channel."
**Explain simply:**
- **UTM tags** are labels on a link (source, medium, campaign) that tell analytics which ad a visitor came from.
- Ad spend and clicks live in the ad platforms; website visits in web analytics; leads and deals in the CRM (customer relationship management system); revenue in orders or finance.
- Each system has its own campaign name, so a mapping table is usually needed.
**Data and tables involved:**
- `ad_spend_daily` (date, platform, campaign_id, impressions, clicks, spend)
- `web_sessions` (session_id, UTM fields, date)
- `leads` (lead_id, created_date, source, campaign)
- `opportunities` or `orders` (amount, stage, close date, lead_id)
- `campaign_map` (campaign names across systems)
- **First cuts:** spend, impressions, clicks, CTR, CPC, leads, cost per lead, customers, revenue, ROAS, by channel, campaign, week and region; then lead-to-customer rate and trend against the previous period.
**Likely follow-ups:** 1) *What if the numbers differ across systems?* Reconcile spend with invoices and agree which system is the source for each metric. 2) *Which date?* State whether you use click, lead or purchase date.
**Common mistakes:** Joining on free-text campaign names; mixing spend dates with revenue dates; reporting clicks and leads but no revenue.

### Q21 ⭐⭐⭐ 🟡 What fields does a CRM opportunity table usually hold, and which data quality problems do you check for first?
**Asked at:** commonly asked (no company-specific report found); CRM data hygiene appears in sales analyst and sales operations guides (unverified).
**What the interviewer is checking:** Whether you know what a deal record contains and distrust it before analysing it.
**Say this in the interview:** "An opportunity holds an id, account, owner, stage, amount, created and expected close date, and source. I check duplicates, missing amounts, impossible dates and stages that were skipped or reset."
**Explain simply:**
- An **opportunity** is a possible sale to an account (a company or customer) that sales is actively working.
- Typical fields (names vary by CRM): opportunity_id, account_id, owner, stage, amount, currency, created_date, expected_close_date, closed_date, status (open, won, lost), loss_reason, lead source, campaign. A **stage history** table records each stage change with a date.
- Data is typed in by salespeople, so it is only as clean as their habits (like a manually filled attendance register).
**Data quality checks first:**
- Duplicate opportunities or accounts.
- Missing or zero amount, wrong currency.
- Close date before created date, or old open deals with a past close date.
- Won deals with no closed date; lost deals with no reason.
- Stage jumps or deals moved backwards; owners who have left.
**Likely follow-ups:** 1) *How do you handle stale deals?* Flag open deals with no activity for a set period and ask the owner. 2) *Overwritten history?* Use stage history or snapshots to see the past.
**Common mistakes:** Computing win rate before cleaning; trusting expected close date; ignoring duplicates.

### Q22 ⭐⭐⭐ 🔴 Paid search reports a ROAS of 6, yet total company revenue has been flat for two months. What could explain this, and what would you check?
**Asked at:** commonly asked (no company-specific report found); the "ROAS looks good but revenue is flat" case appears in marketing analytics guides (unverified).
**What the interviewer is checking:** Whether you doubt a platform-reported metric and think in terms of incrementality.
**Say this in the interview:** "A high ROAS only says attributed revenue is high, not that ads created it. Paid search may be claiming sales that would have happened anyway, so I would check branded searches, double counting and incrementality."
**Explain simply:**
- **Branded search** means people typing your company name; they were already coming, and the ad just captures them.
- **Double counting:** several platforms each claim the same sale.
- **Cannibalisation:** paid search takes credit from free channels such as email or organic search.
- Other causes: spend is small compared with total revenue; other channels fell; returns or cancellations; seasonality; stock-outs; a price or product change.
**Checks, in order:**
- Sum of attributed revenue across platforms compared with actual orders.
- Branded versus non-branded split of paid search.
- New versus returning customers.
- Revenue by channel over the two months, including organic and direct.
- Incrementality: pause or reduce spend in a test region and compare.
**Likely follow-ups:** 1) *How would you prove it?* A holdout or geo test (see Q39 for holdout, geo and before-and-after tests, and Q36 for incrementality). 2) *Would you cut spend?* Only after the test; ROAS 6 might still be incremental for non-branded terms.
**Common mistakes:** Trusting the platform dashboard; comparing ROAS with total revenue directly; changing spend without a test.

### Q23 ⭐⭐⭐ 🔴 The marketing head says a discount campaign worked because sales rose 25% during it. How would you evaluate whether it really worked?
**Asked at:** commonly asked (no company-specific report found); promotion evaluation cases appear in retail analytics guides (unverified).
**What the interviewer is checking:** Whether you ask "compared with what?" and look at profit, not sales.
**Say this in the interview:** "A 25% rise only matters against what would have happened anyway. I would build a baseline, measure incremental sales and gross profit, and check for pulled-forward demand and cannibalisation."
**Explain simply:**
- Build the **baseline** from the same weeks last year, recent trend, or better, a comparison group of stores or customers without the discount.
- **Uplift** is actual minus baseline. Convert it to gross profit, since each unit earns less after a discount (see Q17).
- Subtract campaign costs.
- **Pull-forward:** people bought early or stocked up, so sales fall after the campaign. Compare a few weeks before and after.
- **Cannibalisation:** shoppers switched from full-price products or other categories.
- Also check who bought: new customers, or regulars who would have paid full price?
**Likely follow-ups:** 1) *Best method?* A holdout or geo test, since before-and-after mixes in seasonality. 2) *Long term effect?* Discount-led customers may not return at full price; check repeat rates.
**Common mistakes:** Comparing with the previous week only; judging on revenue; ignoring the post-campaign dip.

### Q24 ⭐⭐⭐ 🔴 Lead volume rose 40% this quarter but sales say lead quality is worse and win rate is down. How do you investigate?
**Asked at:** commonly asked (no company-specific report found); win-rate drop diagnosis appears in sales analyst guides (unverified).
**What the interviewer is checking:** Whether you break the problem down by source and stage before blaming anyone.
**Say this in the interview:** "I would find where the extra leads came from, then compare conversion at each stage by source, segment and rep, to see if quality fell or sales capacity was stretched."
**Explain simply:**
- **Win rate** is deals won divided by deals closed (won plus lost); define it before comparing.
- Split the 40% by source, campaign, region and customer type. A new low-cost source often adds volume of poor leads.
- Follow each group through the funnel: lead to qualified lead, to opportunity, to won. Compare with last quarter.
- Check sales side too: response time to leads, leads per rep, new reps, pricing changes.
- Check timing: this quarter's leads may not have finished their sales cycle, which makes win rate look lower (immature cohorts: leads not yet old enough to have been won or lost).
- Check definitions: did the lead form or scoring rule change?
**Likely follow-ups:** 1) *What do you recommend?* Judge sources by cost per won deal, not cost per lead; tighten or cut weak sources. 2) *How do you stay neutral?* Show the data for both marketing and sales.
**Common mistakes:** Accepting "quality is worse" without proof; comparing unfinished cohorts; looking at the average only.

### Q25 ⭐⭐ 🟢 What is the difference between B2B and B2C marketing and sales analytics in terms of buyers, cycle length and data volume?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know how the business model changes the analysis.
**Say this in the interview:** "B2B sells to companies: few, large, slow, committee-based deals. B2C sells to individuals: many small, fast purchases. So B2B analysis is about pipeline and accounts, B2C about volume and behaviour."
**Explain simply:**
- **B2B** (business to business) example: software sold to a company's HR department. Several people decide, the cycle runs weeks to months, and there are perhaps hundreds of deals.
- **B2C** (business to consumer) example: someone buying shoes online. One person decides in minutes, and there are millions of events.
- B2B data: CRM, deal stages, account-level analysis, small samples. B2C data: clicks, orders, app events; larger samples that suit testing.
- B2B metrics: pipeline, win rate, deal size, cycle length. B2C: conversion, repeat rate, average order value.
**Likely follow-ups:** 1) *Why is A/B testing harder in B2B?* Too few deals for statistical power. 2) *Is there overlap?* Yes, e.g. subscriptions and marketplaces.
**Common mistakes:** Using B2C conversion thinking for long B2B deals; ignoring the buying committee.

### Q26 ⭐⭐ 🟢 What is the difference between paid, owned and earned media, and which channels sit in each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic channel vocabulary.
**Say this in the interview:** "Paid is what we buy, owned is what we control, earned is what others say about us for free."
**Explain simply:**
- **Paid:** search and social ads, display banners, sponsored posts, influencer deals.
- **Owned:** our website, app, blog, email list, our own social pages.
- **Earned:** press coverage, reviews, shares, word of mouth, mentions by others.
- Analysts care because paid has a clear cost, while owned and earned are harder to cost and attribute.
- Boundaries blur: a paid influencer post produces earned shares.
**Likely follow-ups:** 1) *Which is cheapest?* Not simply any; owned still needs content and tools. 2) *How do you measure earned?* Mentions, referral traffic and sentiment, loosely.
**Common mistakes:** Calling social media always paid; ignoring owned channels in ROI.

### Q27 ⭐⭐ 🟢 What is lead scoring, and how is it different from lead status and lead source?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** CRM field vocabulary.
**Say this in the interview:** "Lead scoring ranks how likely a lead is to buy. Status says where the lead is in the process, and source says where it came from."
**Explain simply:**
- **Lead score:** points for fit (company size, job title) and behaviour (visited pricing page, opened emails). High score gets quicker follow-up.
- **Lead status:** New, Contacted, Qualified, Disqualified. It changes over time.
- **Lead source:** Web form, event, referral, paid ad. It is set once, at the start.
- Example: a lead from a webinar (source), recently contacted (status), with 80 points (score).
**Likely follow-ups:** 1) *Who sets the scoring rules?* Marketing and sales together; they must be reviewed against actual wins. 2) *Can it be wrong?* Yes, if the points are guesses.
**Common mistakes:** Mixing the three fields; never checking if high scores really win more.

### Q28 ⭐⭐ 🟢 What is a marketing automation platform (for example Marketo, HubSpot or Salesforce Marketing Cloud), and what kind of data does it produce for an analyst?
**Asked at:** commonly asked (no company-specific report found); these tools appear in analyst job postings (unverified).
**What the interviewer is checking:** Whether you know where campaign data lives.
**Say this in the interview:** "It is software that sends emails and runs nurture journeys automatically, and it records what each contact did, which feeds engagement and lead scoring analysis."
**Explain simply:**
- **Nurture** means a planned series of messages to warm up a lead.
- Data: contact records, email sends, opens, clicks, form fills, landing page visits, campaign membership, lead scores, journey steps, unsubscribes.
- Typically linked to the CRM, so leads and campaign touches can be tied to deals.
- Tool features differ; check the exports available.
**Likely follow-ups:** 1) *Data issues?* Duplicate contacts, bot clicks, differing campaign names. 2) *How does it help attribution?* It logs touches by contact over time.
**Common mistakes:** Trusting open counts; not syncing with CRM.

### Q29 ⭐⭐ 🟢 What is the difference between impressions, reach and frequency in advertising?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic ad metric clarity.
**Say this in the interview:** "Impressions count every time the ad is shown, reach counts how many different people saw it, and frequency is impressions divided by reach."
**Explain simply:**
- Example (invented): an ad shown 1,00,000 times to 25,000 different people has reach 25,000 and frequency 4.
- Impressions are always at least reach.
- Too low a frequency may not register; too high causes fatigue and wasted money.
- Reach depends on the platform's ability to identify unique people, so it is an estimate.
**Likely follow-ups:** 1) *CPM?* Cost per thousand impressions. 2) *Why watch frequency?* Diminishing returns.
**Common mistakes:** Treating impressions as people; averaging frequency without checking spread.

### Q30 ⭐⭐ 🟢 What is the difference between bookings, billings and recognised revenue in a sales organisation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the same sale has different numbers at different times.
**Say this in the interview:** "Bookings is the value of deals signed, billings is what has been invoiced, and recognised revenue is the part earned so far under accounting rules."
**Explain simply:**
- Example (invented): a customer signs a Rs 12,00,000 one-year software contract in January. Bookings: Rs 12,00,000 in January.
- If invoiced upfront, billings are Rs 12,00,000 in January.
- Revenue is recognised as service is delivered: Rs 1,00,000 per month.
- Sales teams use bookings (and quotas), finance uses revenue. Rules vary by company and accounting standard; confirm with finance.
**Likely follow-ups:** 1) *What is cash?* Money actually received, which may come later. 2) *Why matter to analysts?* Reports from sales and finance will not match.
**Common mistakes:** Using the words interchangeably; comparing a sales report with the finance report without reconciling.

### Q31 ⭐⭐ 🟢 What are first-party, second-party and third-party data, and why does the decline of third-party cookies matter to marketing analysts?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand the data privacy shift.
**Say this in the interview:** "First-party is data we collect ourselves, second-party is another company's first-party data shared with us, and third-party is bought from aggregators. Cookie decline makes tracking people across sites harder, so first-party data matters more."
**Explain simply:**
- **First-party:** our purchases, app activity, sign-ups, CRM.
- **Second-party:** a partner's customer data shared through an agreement.
- **Third-party:** data collected by others, such as cookies from many websites, bought or used for ad targeting.
- **Cookies** are small files browsers store to recognise a visitor. As browsers and users restrict third-party ones, cross-site tracking, retargeting and attribution lose coverage.
- Analysts respond with consented first-party data, modelled or aggregated measurement and incrementality tests.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team: privacy laws, including India's data protection law, generally expect clear purpose and consent for using personal data in marketing.
**Likely follow-ups:** 1) *Effect on attribution?* Fewer visible paths, so rely more on tests. 2) *What should a company do?* Collect consented data directly.
**Common mistakes:** Assuming tracking is complete; using personal data without consent.

### Q32 ⭐⭐ 🟢 What are the standard email campaign metrics (delivery rate, open rate, click-through rate, click-to-open rate, bounce, unsubscribe), and why is open rate now an unreliable metric?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can define email metrics precisely and know their limits.
**Say this in the interview:** "Delivery, open, click and unsubscribe rates are all shares of emails sent or delivered. Open rate is unreliable because privacy features can mark emails as opened automatically, so I rely on clicks and conversions."
**Explain simply:**
- **Delivery rate** = delivered / sent. **Bounce rate** = bounced / sent (hard bounce: invalid address; soft: temporary problem).
- **Open rate** = opens / delivered. **CTR** = clicks / delivered. **Click-to-open rate (CTOR)** = clicks / opens.
- **Unsubscribe rate** = unsubscribes / delivered.
- Definitions vary by tool; state yours.
- Some mail apps pre-load images for privacy, which logs an open even if the person never read it, and some block the tracking. So opens are inflated or missing.
**Worked example:** invented figures: 1,00,000 sent, 98,000 delivered, 22,050 opens, 2,450 clicks, 2,000 bounces, 200 unsubscribes. Delivery 98.0%; bounce 2.0%; open 22.5%; CTR 2.5%; CTOR 11.1%; unsubscribe 0.20% (rounded to 1 decimal, except unsubscribe).
**Likely follow-ups:** 1) *What to use instead?* Clicks, conversions and revenue per email. 2) *Why watch unsubscribes?* Rising unsubscribes signal over-mailing.
**Common mistakes:** Mixing sent and delivered as denominators; judging subject lines on open rate alone; counting bot clicks.

### Q33 ⭐⭐ 🟢 What is the difference between MRP, list price, selling price, discount, markup and margin?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you keep price words and profit words apart, especially markup versus margin.
**Say this in the interview:** "MRP, list price and selling price are prices; discount is the gap between two prices; markup and margin are profit measures. Markup is profit over cost, margin is profit over selling price, so for the same sale markup is always the bigger number."
**Explain simply:**
- **MRP (maximum retail price):** in India, the highest price a packaged product may be sold at; printed on the pack (from memory, unverified; confirm with the compliance team).
- **List price:** the price the seller publishes in its catalogue before any offer. It can equal MRP or sit below it.
- **Selling price:** what the customer actually pays. **Discount:** list price minus selling price, usually shown as a percentage of list price.
- **Markup:** (selling price - cost) / cost. **Margin:** (selling price - cost) / selling price.
- Think of an HR parallel: a bonus as a percentage of base salary versus as a percentage of total pay. Same rupees, different denominator.
**Worked example (invented figures, Rs):** MRP and list price 1,000; discount 20%, so selling price = 1,000 x 0.8 = 800; unit cost 600. Profit = 200. Markup = 200 / 600 = **33.3%**. Margin = 200 / 800 = **25%**. Discount = 200 / 1,000 = **20%**. Rounded to one decimal place.
**Likely follow-ups:** 1) *If you want a 25% margin, what markup is needed?* 33.3% on cost. 2) *Is a bigger discount always bigger sales?* No; it also cuts margin (see the discount questions).
**Common mistakes:** Calling a 25% margin a 25% markup; applying a discount percentage to cost instead of to the list price.

### Q34 ⭐⭐ 🟢 What are common promotion types (flat discount, percentage off, buy-one-get-one, coupon, cashback, bundle), and what does each do to the customer's behaviour and the company's margin?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you see every promotion as a trade of margin for behaviour, and know which behaviour each one buys.
**Say this in the interview:** "Each promotion gives up some margin to change what the customer does: buy now, buy more, or come back. Flat and percentage discounts hit margin on every sale, while coupons, cashback and bundles can be targeted, so cost is controlled better."
**Explain simply:**
- **Flat discount (Rs 100 off):** simple; attracts low-price buyers; hurts margin more on cheap items.
- **Percentage off (20% off):** scales with basket size; big on expensive items, so margin loss grows with price.
- **BOGO (buy one, get one free):** pushes units per order and clears stock; effective discount is large (50% on two units at the same price).
- **Coupon:** only people who hold and use it get the offer; lets you target, but existing buyers may use it too (cost without new sales).
- **Cashback:** money returned after purchase, often as wallet credit; pulls the customer back for the next order, and unredeemed credit costs nothing.
- **Bundle:** items sold together at a lower total; raises basket size and can move slow items, but may pull forward sales the customer would have made anyway.
**Likely follow-ups:** 1) *Which protects margin best?* Targeted coupons and bundles, if tested against a control group. 2) *Hidden side effect?* Customers wait for the next offer (stockpiling, pulled-forward demand).
**Common mistakes:** Judging a promotion only by sales lift, ignoring margin and sales borrowed from future weeks.

### Q35 ⭐⭐ 🟢 What is price elasticity of demand, and why do analysts care about it when a discount is planned?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can define elasticity and link it to whether a discount raises revenue.
**Say this in the interview:** "Price elasticity is the percentage change in quantity sold divided by the percentage change in price. If the number is beyond minus 1 in size, demand is elastic and a discount can lift revenue; if it is smaller, a discount just gives money away."
**Explain simply:**
- **Elasticity** = % change in units / % change in price. It is usually negative because price down means units up; analysts often quote the size only.
- **Elastic (size above 1):** customers react strongly, like shoppers on a fashion sale. **Inelastic (size below 1):** customers barely react, like a daily medicine or salt.
- A discount is only worth planning if volume rises enough to cover the lower price per unit (and the lower margin).
- Elasticity differs by product, customer group and time, and measuring it from messy history is hard because other things (festivals, ads) move at the same time.
**Worked example (invented):** price falls 10% and units rise 20%. Elasticity = 20% / -10% = **-2** (elastic). Revenue goes from 1.0 to 0.9 x 1.2 = 1.08, up 8%.
**Likely follow-ups:** 1) *Does higher revenue mean higher profit?* Not necessarily; margin per unit fell too. 2) *Can elasticity be a single number for the whole shop?* No, compute it per category or segment.
**Common mistakes:** Ignoring the sign; assuming elasticity is constant; mixing it up with incrementality.

### Q36 ⭐⭐ 🟢 What is incrementality in marketing, and how is it different from the conversions an ad platform reports?
**Asked at:** commonly asked (no company-specific report found); the internal prep-site sample covers ad-credit versus true-effect cases (unverified as real company questions).
**What the interviewer is checking:** That you know reported conversions are not the same as conversions caused by the ad.
**Say this in the interview:** "Incrementality is the extra sales that happened because of the marketing and would not have happened without it. An ad platform reports conversions it can link to an ad view or click, which includes people who would have bought anyway."
**Explain simply:**
- **Reported (attributed) conversions:** orders the platform matched to an ad exposure within its window.
- **Incremental conversions:** orders in the exposed group minus orders that group would have made without the ad (its baseline).
- Analogy: giving a retention bonus to employees who were never going to resign; they stay, but the bonus did not cause it.
- Retargeting and brand-search ads often look great in reports because they reach people already close to buying.
- You measure incrementality with a control group (holdout or geo test), not with the platform dashboard.
**Likely follow-ups:** 1) *How do you estimate it?* Compare a randomly held-out group with the exposed group. 2) *Is incremental always lower than reported?* Usually, yes, but not guaranteed.
**Common mistakes:** Treating platform ROAS as proof of impact; comparing exposed and unexposed people who differ from the start.

### Q37 ⭐⭐ 🟢 What is lifecycle (CRM) marketing for an app or e-commerce business, and which messages go to a new, active, lapsing and lapsed customer?
**Asked at:** commonly asked (no company-specific report found); CRM-marketing roles appear in the job postings in the sources file.
**What the interviewer is checking:** That you can match message type to where a customer is in their relationship with the brand.
**Say this in the interview:** "Lifecycle marketing sends different messages depending on how recently and how often a customer has bought. New customers get a welcome and a second-order nudge, active ones get recommendations, lapsing ones get a reminder or offer, and lapsed ones get a win-back or are suppressed."
**Explain simply:**
- **CRM marketing:** using customer records (orders, app activity) to message people directly by email, SMS, push or WhatsApp.
- **New:** welcome, how-to, a small incentive for the second purchase (the second order is the key habit-forming moment).
- **Active:** product recommendations, loyalty rewards, new arrivals; no heavy discounts they do not need.
- **Lapsing** (past their normal buying gap, say 60 days for a monthly buyer): "we miss you", reminder of saved cart or favourites, a limited offer.
- **Lapsed:** a final win-back offer; if no response, stop messaging to save cost and protect sender reputation.
- Define the cut-offs from each business's usual repeat gap, not a fixed number.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team: marketing messages need the customer's consent and an easy opt-out; India has separate rules for SMS/calls and a data protection law.
**Likely follow-ups:** 1) *How do you measure success?* Reactivation rate against a holdout. 2) *Which group is cheapest to win?* Usually lapsing, before they fully leave.
**Common mistakes:** Sending the same discount to everyone; ignoring opt-outs; fixed day cut-offs for all products.

### Q38 ⭐⭐ 🟢 What is quota attainment, how is a sales quota usually set, and which data does an analyst need to track it?
**Asked at:** commonly asked (no company-specific report found); quota attainment appears in prep-site sales-ops guides in the sources file (unverified).
**What the interviewer is checking:** Whether you understand attainment as a ratio and know the data behind it.
**Say this in the interview:** "Quota attainment is bookings achieved divided by the quota for the period, as a percentage. Quotas are usually set top-down from the company's revenue target and checked bottom-up against territory potential and past performance."
**Explain simply:**
- **Quota:** the sales target given to a rep or team for a period (month, quarter, year). **Bookings:** the value of deals signed in that period.
- **Top-down:** company target split across teams. **Bottom-up:** based on each territory's customers, pipeline and historical sales. Companies usually reconcile the two; the exact method varies.
- New reps often get lower quotas during a ramp period (the months before they are fully productive), like a probation target in HR.
- Data needed: quota by rep and period (from sales ops), closed-won opportunities with amount, close date and owner, rep start date and territory, and credit rules for split or shared deals.
- Fix the cut-off rule: which date counts (close date or booking date) and whether cancellations are netted off.
**Likely follow-ups:** 1) *Should every rep hit 100%?* Quotas are set so a reasonable share of reps hit them; if almost all do, the quota was probably too low. 2) *Team versus rep attainment?* See the quota-attainment calculation question.
**Common mistakes:** Changing quotas mid-quarter without versioning; ignoring ramping reps, transfers and territory changes when comparing reps.

### Q39 ⭐⭐ 🟢 What is the difference between a holdout test, a geo test and a simple before-and-after comparison for measuring a campaign?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know why a control group beats a before-and-after comparison.
**Say this in the interview:** "A holdout test withholds the campaign from a random slice of customers and compares them with the rest. A geo test does the same by region. A before-and-after compares the same group over time, which is weakest because anything else that changed is mixed in."
**Explain simply:**
- **Holdout:** randomly pick, say, 10% of the customer list who get no message. Difference in purchases between the two groups is the lift. Works when you can control who is exposed.
- **Geo test:** run the campaign in some cities and not in matched others. Used when individuals cannot be controlled (TV, outdoor, broad ads). Needs similar cities and enough of them.
- **Before-and-after:** compare sales last month with this month. Festivals, price changes and seasonality all get credited to the campaign.
- Strength order for a causal claim: holdout, then geo, then before-and-after.
**Likely follow-ups:** 1) *Cost of a holdout?* Some sales are forgone in the held-out group; keep it small but large enough to read. 2) *Can before-and-after ever be fine?* Only as a rough signal with a stable baseline.
**Common mistakes:** Choosing the control group by hand (selection bias); contaminated controls where held-out people still see the ad; stopping the test too early.

### Q40 ⭐⭐ 🟡 A sales team needs to hit a quarterly quota. Using the figures below, calculate the pipeline coverage ratio and the expected bookings, and say whether the pipeline is enough.
Quota Rs 2,00,00,000; open qualified pipeline Rs 6,00,00,000; historical win rate 25%.
**Asked at:** commonly asked (no company-specific report found); pipeline coverage is covered in sales-ops prep guides in the sources file (unverified).
**What the interviewer is checking:** Whether you go beyond coverage to expected value and see that 3x is not automatically enough.
**Say this in the interview:** "Coverage is 3x, but at a 25% win rate the pipeline is expected to produce only Rs 1.5 crore, 75% of the Rs 2 crore quota. So the pipeline is not enough; we need about Rs 8 crore."
**Explain simply:**
- **Pipeline coverage ratio:** open pipeline divided by the quota still to be won. Rules of thumb such as 3x to 4x exist (from memory, unverified), but the right level is 1 divided by your win rate.
- **Expected bookings:** pipeline x win rate.
- Also check that the pipeline closes within the quarter and is truly qualified; old, stuck deals inflate coverage.
**Worked example (Rs):** Coverage = 6,00,00,000 / 2,00,00,000 = **3.0x**. Expected bookings = 6,00,00,000 x 0.25 = **Rs 1,50,00,000** (Rs 1.5 crore), which is 75% of quota; shortfall Rs 50,00,000. Pipeline needed = 2,00,00,000 / 0.25 = **Rs 8,00,00,000** (4x).
**Likely follow-ups:** 1) *What do you do?* Add new pipeline fast, raise win rate on late stages, pull in deals. 2) *Is the 25% reliable?* Check it by stage and by deal source, and over recent quarters.
**Common mistakes:** Saying "3x is healthy" without the win rate; counting pipeline that cannot close by quarter end.

### Q41 ⭐⭐ 🟡 Two channels delivered the leads below. Compare them on cost per lead and cost per qualified lead, and say which you would scale.
Channel A: spend Rs 1,00,000, 1,000 leads, 100 SQLs. Channel B: spend Rs 1,00,000, 400 leads, 120 SQLs.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you judge channels by quality-adjusted cost, not the cheapest lead.
**Say this in the interview:** "A is cheaper per lead at Rs 100 versus Rs 250, but B is cheaper per qualified lead at about Rs 833 versus Rs 1,000. I would scale B, while checking it can take more spend and that its SQLs turn into customers."
**Explain simply:**
- **Lead:** someone who showed interest. **SQL (sales qualified lead):** a lead sales has accepted as worth pursuing.
- **CPL** = spend / leads. **Cost per SQL** = spend / SQLs. The second is closer to real pipeline.
**Worked example (Rs, rounded to the nearest rupee):**
- Channel A: CPL = 1,00,000 / 1,000 = **100**; cost per SQL = 1,00,000 / 100 = **1,000**; SQL rate = 10%.
- Channel B: CPL = 1,00,000 / 400 = **250**; cost per SQL = 1,00,000 / 120 = **833**; SQL rate = 30%.
**Likely follow-ups:** 1) *What else before scaling?* SQL-to-won rate, deal size, and whether extra spend keeps the same cost (diminishing returns). 2) *Would you stop A?* Not necessarily; test lowering its volume or improving its form quality.
**Common mistakes:** Optimising on cost per lead alone, which rewards low-quality leads; assuming average cost equals the cost of the next lead.

### Q42 ⭐⭐ 🟡 Calculate delivery rate, open rate, click-through rate (on delivered) and click-to-open rate for the email campaign below.
Sent 50,000; delivered 48,000; unique opens 14,400; unique clicks 1,920; unsubscribes 96.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you use the right denominator for each email metric.
**Say this in the interview:** "Delivery is 96%, open rate is 30% of delivered, click-through is 4% of delivered, and click-to-open is 13.3% of opens. Each uses a different denominator, so I always state it."
**Explain simply:**
- **Delivery rate** = delivered / sent. **Open rate** = unique opens / delivered. **CTR** = unique clicks / delivered. **CTOR (click-to-open rate)** = unique clicks / unique opens.
- Definitions vary by tool (some use sent as the base); I use delivered.
- Open counts can be inflated because some mail apps pre-load images automatically (from memory, unverified), so clicks are the safer signal.
**Worked example (rounded to one decimal place):**
- Delivery rate = 48,000 / 50,000 = **96.0%** (bounced: 2,000, 4.0% of sent)
- Open rate = 14,400 / 48,000 = **30.0%**
- CTR = 1,920 / 48,000 = **4.0%**
- CTOR = 1,920 / 14,400 = **13.3%**
- Unsubscribe rate = 96 / 48,000 = **0.2%**
**Likely follow-ups:** 1) *Why is CTOR useful?* It judges the content among people who opened. 2) *Is 0.2% unsubscribe bad?* Compare with your own past campaigns.
**Common mistakes:** Dividing every metric by sent; mixing unique and total opens; reading CTR and CTOR as the same thing.

### Q43 ⭐⭐ 🟡 Score the six customers below on R, F and M (1 to 3, 3 best, ranked within this small group) and name which one is a champion, which one is at risk and which one is new.
C1: last order 5 days ago, 12 orders, Rs 30,000. C2: 200 days, 8 orders, Rs 18,000. C3: 10 days, 1 order, Rs 800. C4: 40 days, 4 orders, Rs 6,000. C5: 300 days, 1 order, Rs 500. C6: 20 days, 6 orders, Rs 9,000.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you score recency in the right direction and read the score pattern as a customer story.
**Say this in the interview:** "I rank each measure and split the six into three pairs. C1 scores 3-3-3, a champion; C2 scores 1-3-3, a big past customer who has gone quiet, so at risk; C3 scores 3-1-1, a recent first-time buyer, so new."
**Explain simply:**
- **R (recency):** days since last order, where fewer days is better. **F (frequency):** number of orders. **M (monetary):** total spend.
- With six customers, the top two on each measure get 3, the middle two get 2, the bottom two get 1. Orders tie for C3 and C5 (1 each), so they share the bottom score.
- Real projects use more customers and quintiles (1 to 5) or business-defined cut-offs.
**Worked example:**

| Customer | R | F | M | Score | Label |
|---|---|---|---|---|---|
| C1 | 3 | 3 | 3 | 333 | Champion |
| C2 | 1 | 3 | 3 | 133 | At risk (high value, 200 days silent) |
| C3 | 3 | 1 | 1 | 311 | New (one recent order) |
| C4 | 2 | 2 | 2 | 222 | Average |
| C5 | 1 | 1 | 1 | 111 | Lost |
| C6 | 2 | 2 | 2 | 222 | Average |

Ranks: recency order C1 (5), C3 (10), C6 (20), C4 (40), C2 (200), C5 (300); frequency order C1, C2, C6, C4, then C3 and C5; money order C1, C2, C6, C4, C3, C5.
**Likely follow-ups:** 1) *What would you do for C2?* A personal win-back message. 2) *For C3?* Nudge a second order.
**Common mistakes:** Giving 3 to the longest recency; letting one big spender hide a lapsed customer; fixed score cut-offs that do not fit the business.

### Q44 ⭐⭐ 🟡 After a price cut from Rs 100 to Rs 90, monthly units rose from 1,000 to 1,200. Calculate the price elasticity and say whether revenue rose or fell.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you compute percentage changes correctly and tie elasticity to revenue.
**Say this in the interview:** "Price fell 10%, units rose 20%, so elasticity is minus 2: demand is elastic. Revenue rose from Rs 1,00,000 to Rs 1,08,000, up 8%."
**Explain simply:**
- Elasticity = % change in units / % change in price. Size above 1 means a price cut raises revenue.
- A revenue rise does not mean a profit rise; check unit margin too.
- This is two points, so it may also reflect other changes (season, ads). Treat it as a rough estimate.
**Worked example (Rs):**
- % change in price = (90 - 100) / 100 = **-10%**; % change in units = (1,200 - 1,000) / 1,000 = **+20%**.
- Elasticity = 20 / -10 = **-2.0**.
- Revenue before = 100 x 1,000 = **1,00,000**; after = 90 x 1,200 = **1,08,000**; change = +8,000, **+8%**.
- Midpoint method (uses averages as base) gives **-1.73**; the conclusion is the same.
**Likely follow-ups:** 1) *Which method do you report?* The simple one, and say so. 2) *What if margin is 15%?* Check gross profit: it can fall even if revenue rises.
**Common mistakes:** Using the new price as the base; reporting percentage points; forgetting to check profit.

### Q45 ⭐⭐ 🟡 Four reps have the quotas and bookings below. Calculate each rep's attainment, the team attainment, and explain why the average of rep attainments differs from team attainment.
R1: quota 50, booked 60. R2: quota 50, booked 25. R3: quota 100, booked 90. R4: quota 20, booked 40. (Rs lakh)
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know team attainment is weighted by quota, and a simple average is not.
**Say this in the interview:** "Rep attainments are 120%, 50%, 90% and 200%. Team attainment is 215 over 220, which is 97.7%. The simple average of reps is 115%, because it treats the small Rs 20 lakh quota rep the same as the Rs 100 lakh one."
**Explain simply:**
- Attainment = booked / quota. Team attainment = total booked / total quota.
- The average of percentages gives every rep equal weight, regardless of quota size. Team attainment weights each rep by quota.
- The same trap appears in HR: average of department attrition rates is not company attrition.
**Worked example (Rs lakh, rounded to one decimal):**
- R1 60 / 50 = **120%**; R2 25 / 50 = **50%**; R3 90 / 100 = **90%**; R4 40 / 20 = **200%**.
- Team: booked 60 + 25 + 90 + 40 = 215; quota 50 + 50 + 100 + 20 = 220; attainment = **97.7%**.
- Simple average of rep attainments = (120 + 50 + 90 + 200) / 4 = **115%**.
**Likely follow-ups:** 1) *Which number goes to leadership?* Team attainment, with the rep spread alongside. 2) *Anything about R4?* A small quota inflates the percentage; look at rupees too.
**Common mistakes:** Averaging percentages; capping attainment at 100% for some reps but not others without saying so.

### Q46 ⭐⭐ 🟡 Calculate pipeline velocity and say which of the four inputs you would try to improve first.
Qualified opportunities 200; win rate 20%; average deal size Rs 5,00,000; average sales cycle 80 days.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the formula and understand which lever is cheapest to move.
**Say this in the interview:** "Velocity is 200 x 20% x Rs 5,00,000 / 80 days, which is Rs 2,50,000 of expected revenue per day. Because the formula multiplies, a 10% gain in any of the first three inputs gives the same lift, so I would start with the one that is easiest to move, usually win rate through better qualification."
**Explain simply:**
- **Pipeline velocity:** how much revenue the pipeline is expected to produce per day: (opportunities x win rate x deal size) / sales cycle days.
- Three inputs raise it (opportunities, win rate, deal size); a shorter cycle also raises it.
- Choose by cost and control: more opportunities cost marketing spend; larger deals need pricing and product changes; a faster cycle needs process fixes; win rate often improves with better qualification and follow-up.
**Worked example (Rs):** Velocity = 200 x 0.20 x 5,00,000 / 80 = 2,00,00,000 / 80 = **Rs 2,50,000 per day**; over 90 days about Rs 2.25 crore. Raising any one of opportunities, win rate or deal size by 10% gives Rs 2,75,000 per day; cutting the cycle to 72 days gives about Rs 2,77,778.
**Likely follow-ups:** 1) *Is it a forecast?* No, it is a snapshot rate that assumes the inputs stay stable. 2) *Can raising one input hurt another?* Yes, chasing more leads can lower win rate.
**Common mistakes:** Mixing cycle length in months with daily results; including unqualified opportunities; changing one lever while ignoring the effect on another.

### Q47 ⭐⭐ 🟡 Calculate the weighted pipeline for the quarter from the stage probabilities below, and explain why it is not a promise.
Prospecting Rs 4 crore at 10%; Proposal Rs 3 crore at 30%; Negotiation Rs 2 crore at 60%; Contract sent Rs 1 crore at 90%.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can compute a probability-weighted total and describe its limits.
**Say this in the interview:** "Weighted pipeline is Rs 3.4 crore out of Rs 10 crore of raw pipeline. It is an average expected value across many deals, not a promise for any one deal, and the stage probabilities may not match reality."
**Explain simply:**
- Weighted pipeline = sum of (stage amount x stage probability).
- Each deal either closes fully or not at all; the weighted number only holds on average across many deals.
- Stage probabilities are often set by default in the CRM and not checked against actual history; also, not all pipeline closes within this quarter.
**Worked example (Rs crore):** 4 x 0.10 = 0.4; 3 x 0.30 = 0.9; 2 x 0.60 = 1.2; 1 x 0.90 = 0.9. Total = **Rs 3.4 crore**, which is 34% of the Rs 10 crore raw pipeline.
**Likely follow-ups:** 1) *How do you test the probabilities?* Compare them with historical stage-to-won rates. 2) *Range instead of one number?* Yes, show low and high cases.
**Common mistakes:** Presenting weighted pipeline as a commitment; adding raw and weighted figures together.

### Q48 ⭐⭐ 🟡 A coupon campaign issued 20,000 coupons of Rs 50; 3,000 were redeemed, and a matched control group suggests 1,800 of those orders would have happened anyway. Calculate the redemption rate and the cost per incremental order.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you separate coupon use from coupon impact and cost the full discount.
**Say this in the interview:** "Redemption is 15%. Incremental orders are 3,000 minus 1,800, which is 1,200. The company paid Rs 1,50,000 in discounts, so each truly extra order cost Rs 125, not Rs 50."
**Explain simply:**
- **Redemption rate** = redeemed coupons / issued coupons.
- **Incremental orders** = redeemed orders minus orders that would have happened anyway (the control-group baseline).
- Cost is the discount given on all redeemed coupons, including to people who would have bought anyway.
- Compare Rs 125 with the margin on an order: if gross profit per order is below that, the campaign lost money on this basis.
**Worked example (Rs):** Redemption = 3,000 / 20,000 = **15%**. Incremental orders = 3,000 - 1,800 = **1,200** (40% of redemptions). Total discount cost = 3,000 x 50 = **1,50,000**. Cost per incremental order = 1,50,000 / 1,200 = **Rs 125**; naive cost per redeemed order = Rs 50.
**Likely follow-ups:** 1) *Other costs?* Message and tool costs, and any later sales pulled forward. 2) *Make it cheaper?* Target people unlikely to buy without the coupon.
**Common mistakes:** Dividing cost by all redemptions; ignoring that 60% of the redemptions were subsidy for existing demand.

### Q49 ⭐⭐ 🟡 A campaign had 30,00,000 impressions reaching 10,00,000 unique people with a spend of Rs 1,50,000. Calculate the average frequency, CPM and cost per reached person, and say what frequency you would worry about.
**Asked at:** commonly asked (no company-specific report found); campaign metric calculations appear in marketing analyst guides (prep-site level, unverified).
**What the interviewer is checking:** Whether you know impressions, reach and frequency apart, and whether you know an average can hide a problem.
**Say this in the interview:** "Frequency is 3, CPM is Rs 50 and it cost 15 paise to reach one person. I would not judge frequency by the average; I would look at how results change as people see the ad more often."
**Explain simply:**
- **Impression:** one time an ad is shown on a screen. **Reach:** how many different people saw it at least once. **Frequency:** impressions divided by reach, the average number of times each reached person saw the ad.
- **CPM** (cost per mille, "mille" means thousand) is the cost of 1,000 impressions.
- An average of 3 can mean everyone saw it 3 times, or most saw it once while a small group saw it 20 times. The second case wastes money and annoys people (ad fatigue).
- There is no single "bad" frequency. Commonly quoted fatigue points are somewhere around 5 to 7 views a week (from memory, unverified); it depends on the product and platform. Find your own: split reached people by number of views and check click or conversion rate in each bucket. Worry where results flatten or drop while cost keeps rising.
**Worked example:** (computed by script, no rounding needed)
- Frequency = 30,00,000 / 10,00,000 = 3.0 impressions per person.
- CPM = 1,50,000 / 30,00,000 x 1,000 = Rs 50.
- Cost per reached person = 1,50,000 / 10,00,000 = Rs 0.15 (equals CPM Rs 50 divided by frequency 3, and 1,000 reached people cost Rs 150).
**Likely follow-ups:** 1) *Is reach the same across platforms?* No; each platform counts its own users, so the same person can be counted on two. 2) *What would you do about high frequency?* Cap the frequency, rotate creatives, or widen the audience.
**Common mistakes:** Calling impressions "people reached"; dividing spend by impressions and forgetting to multiply by 1,000 for CPM; judging only the average.

### Q50 ⭐⭐ 🟡 Customers are grouped by value below. Calculate each group's share of customers and revenue and say what it implies for the retention budget.
Top 10% of customers: Rs 55 lakh. Next 30%: Rs 30 lakh. Bottom 60%: Rs 15 lakh. Total 10,000 customers.
**Asked at:** commonly asked (no company-specific report found); value-based segmentation is a standard marketing analyst topic (unverified, prep-site level).
**What the interviewer is checking:** Whether you can turn a skewed distribution into a spending decision, not just percentages.
**Say this in the interview:** "The top 10% of customers bring 55% of revenue, so I would weight retention spend by value at risk, with the strongest protection for the top group, but not ignore the middle 30%."
**Explain simply:**
- Total revenue is 55 + 30 + 15 = Rs 100 lakh, so each lakh figure is also its percentage share.
- Revenue is not profit. A big customer who needs heavy discounts may earn less than the revenue suggests, so I would check margin before finalising the budget.
- The retention budget is money spent to stop existing customers leaving. Losing one top customer costs far more than losing one bottom customer, so equal spend per head is wasteful.
- The middle 30% often has the best upside: moving some of them up a tier is cheaper than finding new top customers.
**Worked example:** (computed by script)

| Group | Customers | Share of customers | Revenue | Share of revenue | Revenue per customer |
|---|---|---|---|---|---|
| Top 10% | 1,000 | 10% | Rs 55 lakh | 55% | Rs 5,500 |
| Next 30% | 3,000 | 30% | Rs 30 lakh | 30% | Rs 1,000 |
| Bottom 60% | 6,000 | 60% | Rs 15 lakh | 15% | Rs 250 |

A top customer is worth 5,500 / 250 = 22 times a bottom customer. Top 40% together give 85% of revenue. (Revenue per customer is for the period of the data, which the question does not state.)
**Likely follow-ups:** 1) *Would you give 55% of the budget to the top group?* Not mechanically; I would use churn risk and margin as well, since spending on someone unlikely to leave is wasted. 2) *How do you build such groups?* Rank customers by revenue or profit over a fixed period and cut into percentiles.
**Common mistakes:** Treating "Pareto 80/20" as a law; ignoring margin; giving the bottom 60% zero attention without checking cheap automated options.

### Q51 ⭐⭐ 🟡 Marketing spent Rs 5,00,000 and the sales attributed to the campaign produced Rs 14,00,000 revenue at 35% gross margin. Calculate ROAS and marketing ROI on gross profit.
**Asked at:** commonly asked (no company-specific report found); ROAS-looks-good-but-loses-money cases appear in marketing analyst guides (unverified, prep-site level).
**What the interviewer is checking:** Whether you know ROAS is revenue-based and ignores margin, and that a healthy-looking ROAS can still lose money.
**Say this in the interview:** "ROAS is 2.8 times, which sounds fine, but at 35% margin the campaign earned Rs 4,90,000 of gross profit on Rs 5,00,000 spend, so ROI is about minus 2%."
**Explain simply:**
- **ROAS** (return on ad spend) = revenue / ad spend. It says nothing about product cost.
- **Gross margin** is the share of revenue left after the direct cost of the goods, so gross profit = revenue x margin.
- **Marketing ROI** here = (gross profit minus spend) / spend. Companies define ROI differently (some use revenue, some net profit); I state mine.
- Break-even ROAS = 1 / margin = 1 / 0.35 = 2.86. Anything below that loses money before other costs.
**Worked example:** (computed by script)
- ROAS = 14,00,000 / 5,00,000 = 2.8x.
- Gross profit = 14,00,000 x 0.35 = Rs 4,90,000.
- Net gain = 4,90,000 - 5,00,000 = minus Rs 10,000.
- ROI = minus 10,000 / 5,00,000 = minus 2.0%.
**Likely follow-ups:** 1) *Would you stop the campaign?* Not on this alone; check whether the sales were incremental and what repeat purchases follow (customer lifetime value). 2) *Is attributed revenue reliable?* It depends on the attribution rule; some of it may have happened anyway.
**Common mistakes:** Calling ROAS the profit; using revenue instead of gross profit in ROI; confusing 2.8x with 280% profit.

### Q52 ⭐⭐ 🟡 Compare buying on CPM and buying on CPC for the two ad channels below, and say which gives the cheaper click and the cheaper lead.
Channel X: CPM Rs 80, CTR 1.0%, click-to-lead 5%. Channel Y: CPM Rs 150, CTR 3.0%, click-to-lead 4%.
**Asked at:** commonly asked (no company-specific report found); channel cost comparison is common in marketing analyst guides (unverified, prep-site level).
**What the interviewer is checking:** Whether you can convert between pricing models and not be fooled by the cheapest CPM.
**Say this in the interview:** "Channel Y has the higher CPM but the cheaper click (Rs 5 against Rs 8) and the cheaper lead (Rs 125 against Rs 160), because far more people click."
**Explain simply:**
- **CPM:** you pay per 1,000 impressions. **CPC** (cost per click): you pay only when someone clicks. **CTR** (click-through rate) = clicks / impressions. **CPL** (cost per lead): spend / leads.
- Convert everything to a common base: per 1,000 impressions, effective CPC = CPM / (1,000 x CTR), and CPL = effective CPC / click-to-lead rate.
- Buying on CPC moves the risk of a weak ad (low CTR) to the platform; buying on CPM leaves it with you.
**Worked example:** (computed by script)

| | Channel X | Channel Y |
|---|---|---|
| Clicks per 1,000 impressions | 10 | 30 |
| Effective CPC | 80 / 10 = Rs 8 | 150 / 30 = Rs 5 |
| Leads per 1,000 impressions | 0.5 | 1.2 |
| CPL | 80 / 0.5 = Rs 160 | 150 / 1.2 = Rs 125 |

With Rs 1,00,000 spend: X gives 12,500 clicks and 625 leads; Y gives 20,000 clicks and 800 leads.
**Likely follow-ups:** 1) *Does the cheaper lead mean better?* Not yet; compare lead quality (how many become customers), as Y's leads might be weaker. 2) *Could CTR change at scale?* Yes, reaching more people usually lowers CTR.
**Common mistakes:** Picking the lowest CPM; mixing percentages (1.0% is 0.01); stopping at cost per lead without cost per customer.

### Q53 ⭐⭐ 🟡 Leads scored above 70 and below 70 converted as below. Calculate the conversion rate of each group and the lift, and say whether the score is useful.
Score above 70: 1,000 leads, 150 converted. Score 70 or below: 4,000 leads, 100 converted.
**Asked at:** commonly asked (no company-specific report found); lead scoring and lead quality appear in sales and marketing analyst guides (unverified, prep-site level).
**What the interviewer is checking:** Whether you compare rates (not counts), understand lift, and ask whether the score really causes better outcomes.
**Say this in the interview:** "High-score leads convert at 15% against 2.5% for the rest, a 6 times lift, so the score separates leads well. I would still check it is not just reflecting where sales effort goes."
**Explain simply:**
- A **lead score** is a number given to each enquiry from its profile and behaviour, to help sales decide who to call first.
- **Conversion rate** = converted / leads. **Lift** here = rate of one group divided by rate of the other (some people instead compare a group with the overall average; I state which).
- The percentage-point gap is 12.5 points; the ratio is 6 times. Both are useful; the ratio is bigger when rates are small.
**Worked example:** (computed by script)
- Above 70: 150 / 1,000 = 15.0%. 70 or below: 100 / 4,000 = 2.5%. Overall: 250 / 5,000 = 5.0%.
- Lift = 15.0 / 2.5 = 6.0 times (versus overall: 3 times).
- The high group is 20% of leads but 60% of conversions (150 / 250).
- Not to ignore: 100 conversions, 40% of the total, still came from the low group.
**Likely follow-ups:** 1) *What could mislead you?* If sales called high-score leads faster, the score may look better than it is; use a holdout or compare time-to-contact. 2) *Would you stop calling low-score leads?* Not outright; move them to cheaper nurturing (automated emails).
**Common mistakes:** Comparing 150 with 100 conversions instead of rates; calling the score "accurate" without testing it on new leads.

### Q54 ⭐⭐ 🟡 Two discount depths were tested on similar deals. Which would you recommend and why?
10% discount: 200 deals, win rate 30%, average price after discount Rs 90,000 at 40% margin. 20% discount: 200 deals, win rate 36%, average price after discount Rs 80,000 at 30% margin.
**Asked at:** commonly asked (no company-specific report found); discount and pricing trade-offs appear in sales analyst guides (unverified, prep-site level).
**What the interviewer is checking:** Whether you judge by total gross profit, not by win rate or revenue.
**Say this in the interview:** "I would recommend the 10% discount. The deeper discount wins 12 more deals, but total gross profit falls from Rs 21.6 lakh to Rs 17.28 lakh."
**Explain simply:**
- **Win rate** is the share of deals that close. A deeper discount raises it but cuts the price and the margin on each deal.
- I compare gross profit per 200 deals = deals x win rate x price x margin.
- Both arms imply the same full price of Rs 1,00,000 (90,000 / 0.9 and 80,000 / 0.8). The implied unit cost differs slightly (Rs 54,000 in the first arm, Rs 56,000 in the second), so I would confirm the margins; if both arms had the Rs 54,000 cost, the 20% arm would earn Rs 18.72 lakh, still below Rs 21.6 lakh.
**Worked example:** (computed by script)

| | 10% discount | 20% discount |
|---|---|---|
| Wins | 200 x 30% = 60 | 200 x 36% = 72 |
| Revenue | 60 x 90,000 = Rs 54,00,000 | 72 x 80,000 = Rs 57,60,000 |
| Gross profit per win | Rs 36,000 | Rs 24,000 |
| Gross profit | Rs 21,60,000 | Rs 17,28,000 |

The 20% option has higher revenue (+Rs 3.6 lakh) but lower profit (minus Rs 4.32 lakh). For 20% to match, its win rate would need to be 45% (computed), far above 36%.
**Likely follow-ups:** 1) *Is the difference real?* With 200 deals per arm, 30% against 36% could be chance; I would run a significance test and check the deals were truly comparable. 2) *Anything beyond profit?* Discounts can set a price expectation for renewals, and faster closing may have value.
**Common mistakes:** Choosing the higher win rate or revenue; forgetting the margin changes with the discount.

### Q55 ⭐⭐ 🟡 How do you join ad platform spend data with CRM leads and orders, and what breaks in the join?
**Asked at:** commonly asked (no company-specific report found); joining spend to CRM outcomes is a core marketing analytics task in job descriptions (unverified, prep-site level).
**What the interviewer is checking:** Whether you know the join keys, the grain (what one row means), and why totals go wrong.
**Say this in the interview:** "I summarise each source to the same grain, usually campaign and date, clean the campaign keys, and then join. What breaks is mismatched keys, missing tags, duplicated rows and time lags."
**Explain simply:**
- Ad platforms (Google, Meta) give spend, clicks and impressions by campaign and day. The CRM (customer relationship management system) holds leads and orders. They share no customer ID; the bridge is the **UTM tags** (labels such as utm_campaign added to the ad link) stored on each lead, or a click ID.
- **Grain:** spend is one row per campaign per day; leads are one row per person. Joining them raw repeats the spend on every lead. Always aggregate first.
- What breaks: inconsistent spelling or case in campaign names; leads with no tag (direct, phone, offline); the same campaign name reused; time zones and attribution lag (a lead today from a click last week); currency or tax-inclusive spend; duplicate leads.
**Worked example:** a small test (invented data, run in SQLite) shows the pattern; note the cleaning with `upper(trim())`.
```sql
-- summarise spend and leads to campaign level first, then join
with spend as (
  select upper(trim(campaign_id)) as campaign, sum(spend) as spend
  from ad_spend group by 1),
leads as (
  select upper(trim(utm_campaign)) as campaign, count(distinct l.lead_id) as leads,
         count(o.order_id) as orders, coalesce(sum(o.order_value), 0) as revenue
  from crm_leads l left join orders o on o.lead_id = l.lead_id
  group by 1)
select s.campaign, s.spend, l.leads, l.orders, l.revenue,
       round(1.0 * s.spend / l.leads, 1) as cost_per_lead
from spend s left join leads l on l.campaign = s.campaign;
```
Output: C1 spend 2,200, 3 leads, 2 orders, revenue 8,000, cost per lead 733.3; C2 spend 800, 1 lead, 0 orders, cost per lead 800. One lead had no tag and fell outside both rows, which is exactly the "unattributed" gap to report.
**Likely follow-ups:** 1) *Why a left join from spend?* So campaigns that spent money but got no leads still show up. 2) *How do you report untagged leads?* As their own "unattributed" line, not forced into a campaign.
**Common mistakes:** Joining at lead level and summing spend (inflates spend); not trimming or lower-casing keys; ignoring untagged leads.

### Q56 ⭐⭐ 🟡 What data would you gather for a customer segmentation project, and what first cuts would you run before choosing segments?
**Asked at:** commonly asked (no company-specific report found); segmentation questions appear in marketing analyst guides (unverified, prep-site level).
**What the interviewer is checking:** Whether you start from the business purpose and explore the data before forcing a method.
**Say this in the interview:** "I would first ask what decision the segments feed, then gather transactions, customer profile and engagement data, and look at simple distributions before any clustering."
**Explain simply:**
- **Segmentation** means splitting customers into groups that behave differently so each can be treated differently (offers, channels, service).
- Purpose first: segments for retention need different data from segments for new-product targeting.
- If this were HR: grouping employees by tenure, role and attendance to design different engagement actions.
**Data and tables involved:**
- Customers (ID, sign-up date, city, age band if collected and allowed), orders (date, value, product category, discount, channel, returns), engagement (email opens, app visits, support tickets), and consent flags.
- **First cuts:** distribution of orders and revenue per customer (how skewed); recency (days since last order), frequency and monetary value (the **RFM** method); split by acquisition channel, city, category; share of one-time buyers; missing data counts.
- Then test candidate segments: are they large enough, stable over months, clearly different on a key metric, and can marketing actually act on them?
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the compliance/legal team: use only data for which the customer gave consent for that purpose, and avoid sensitive attributes unless clearly justified.
**Likely follow-ups:** 1) *Rules or clustering?* Start with simple rules (RFM); use clustering such as k-means (a standard method that groups similar customers automatically) if rules do not capture differences. 2) *How do you know segments are good?* They differ on outcomes and a different action is possible per segment.
**Common mistakes:** Clustering before cleaning; segments too many to act on; ignoring that outliers dominate a segment.

### Q57 ⭐⭐ 🟡 What data would you need to measure whether a promotion was profitable, and what first cuts would you run?
**Asked at:** commonly asked (no company-specific report found); promotion and uplift measurement is common in retail and e-commerce analyst guides (unverified, prep-site level).
**What the interviewer is checking:** Whether you think in baseline versus actual, margin, and side effects rather than sales alone.
**Say this in the interview:** "I would compare profit during the promotion with what would have happened without it, a baseline or a control group, after subtracting discount cost and side effects such as pulling sales forward."
**Explain simply:**
- **Baseline:** the sales you expected without the promotion. **Uplift:** actual minus baseline. **Incremental profit:** uplift in profit after discount and campaign cost.
- Side effects: **cannibalisation** (customers switch from a similar product), **stockpiling or pull-forward** (they buy now, less later), and customers who would have bought at full price anyway.
**Data and tables involved:**
- Sales lines (date, product, store or channel, units, price, discount, unit cost), promotion calendar (which items, where, when), customer IDs if available, campaign costs, and a comparison group (similar stores or customers without the promotion).
- **First cuts:** units and gross profit before, during and after the promotion; promoted against control; sales of related products; new versus existing customers; discount cost per incremental order; the dip after the promotion ends.
- Tip: compare at least several weeks before and after, to catch the dip.
**Likely follow-ups:** 1) *No control group exists, what do you do?* Use previous weeks, same period last year, or similar stores as a rough baseline and state the limit. 2) *Is higher revenue enough?* No; a promotion can raise revenue and cut profit.
**Common mistakes:** Comparing promotion week with a normal week and calling the whole gap uplift; ignoring cost of the discount on units that would have sold anyway.

### Q58 ⭐⭐ 🟡 Why does a pipeline analysis need a stage-history (snapshot) table and not only the current CRM opportunity table?
**Asked at:** commonly asked (no company-specific report found); pipeline reporting is a standard sales analyst topic (unverified, prep-site level).
**What the interviewer is checking:** Whether you understand that the CRM overwrites the past, so history needs to be stored separately.
**Say this in the interview:** "The opportunity table only shows where each deal is now. To know what the pipeline looked like last month, how long deals sat in each stage, or where they dropped out, I need stage history or regular snapshots."
**Explain simply:**
- The **pipeline** is the list of open sales opportunities and the value in each stage (for example prospecting, proposal, negotiation, won or lost).
- A CRM row for an opportunity is updated in place: when a deal moves from proposal to negotiation, the stage field simply changes and the earlier stage is lost (unless field history tracking is on).
- A **snapshot table** stores a copy of every open opportunity on a regular date (daily or weekly). A **stage-history table** stores a row each time the stage changes, with date.
- Like HR: a headcount table that only shows today's employees cannot tell you last quarter's headcount or why people left.
**Worked example:** (conceptual, no calculation needed) A deal worth Rs 10 lakh is in negotiation today. Without history you cannot say whether it entered the quarter as a proposal, how many days it spent in each stage, or whether the pipeline at the start of the quarter was big enough to hit target (pipeline coverage). With snapshots you can compare pipeline on day 1 with revenue won by day 90.
**Likely follow-ups:** 1) *What would you analyse with it?* Stage conversion rates, time in stage (velocity), pipeline growth week by week, slippage of close dates. 2) *Alternatives?* CRM field history, or event logs, if available.
**Common mistakes:** Calculating win rate or stage conversion from current stages only (survivorship bias: deals that left are invisible); not recording deal value changes.

### Q59 ⭐⭐ 🟡 How do duplicate leads and contacts arise across a CRM, a marketing automation tool and web forms, and how do they distort funnel metrics?
**Asked at:** commonly asked (no company-specific report found); CRM data quality is common in marketing operations job descriptions (unverified, prep-site level).
**What the interviewer is checking:** Whether you understand data quality and its impact on counts and rates.
**Say this in the interview:** "The same person enters through several systems with small differences, such as a different email, so one person is counted several times. That inflates leads, lowers conversion rates and breaks cost per lead."
**Explain simply:**
- **How duplicates arise:** the same person fills two web forms; uses a work and a personal email; is typed differently by a sales rep (name or phone format); is imported from an event list; or the marketing automation tool (software that sends emails and tracks behaviour) and the CRM each create a record and sync imperfectly.
- **Effects:**
  - Lead counts rise, so cost per lead looks lower than the cost per unique person.
  - Conversion rate falls because only one of the duplicates converts.
  - Email metrics distort: the same person gets two emails, and one may complain.
  - Sales reps chase the same person, and ownership gets confused.
- **Handling:** define a **match key** (normalised email, phone), merge or flag duplicates, keep the earliest created date for first-touch reporting, and report unique people alongside raw records.
**Likely follow-ups:** 1) *How do you find duplicates?* Count by lower-cased trimmed email, then phone plus name; use fuzzy matching for the rest. 2) *Which record survives?* A rule such as most recent activity or most complete record, agreed with the CRM owner.
**Common mistakes:** Deduplicating only on exact email; deleting records instead of merging (history lost); reporting conversion without stating the unit (leads or unique people).

### Q60 ⭐⭐ 🟡 What is the difference between Google Analytics sessions, ad platform clicks and CRM leads, and why do the three numbers rarely match?
**Asked at:** commonly asked (no company-specific report found); reconciling these sources is a common marketing analytics problem in guides (unverified, prep-site level).
**What the interviewer is checking:** That you know each source counts a different thing, at a different point, with its own rules.
**Say this in the interview:** "A click is an ad platform event, a session is a website visit recorded by the analytics tool, and a lead is a person who filled a form in the CRM. Each step loses or adds counts, so the numbers differ by design."
**Explain simply:**
- **Ad platform click:** counted when someone clicks the ad, before the page loads. **Session:** a group of visits to your site in one go, counted by the analytics tool (Google Analytics) only if the page loaded and the tracking code ran and was allowed.
- **CRM lead:** a person record created when they submit a form or are added manually.
- Why they differ:
  - Visitors click but leave before the page loads, or block tracking or reject cookies.
  - Invalid clicks and double clicks may be counted or filtered differently.
  - One click can lead to several sessions, or several clicks to one session.
  - Different time zones, attribution windows and definitions of "session".
  - Leads come from many places (phone, events, offline), and duplicates or test leads exist.
- **What I do:** treat them as a funnel with expected drop at each step, track the ratio over time (clicks to sessions), and investigate when the ratio changes suddenly, such as a tracking tag breaking.
**Likely follow-ups:** 1) *Which number do you trust for spend?* The ad platform (it is billed) and for outcomes the CRM. 2) *What gap would worry you?* A sudden change in click-to-session ratio.
**Common mistakes:** Expecting them to be equal; picking one source without saying which; forgetting that tracking consent reduces sessions.

### Q61 ⭐⭐ 🟡 In plain words, what does India's data protection law (DPDP Act) mean for a marketing team's customer data and consent? (from memory, awareness level)
**Asked at:** commonly asked (no company-specific report found); privacy awareness is increasingly raised in marketing analyst roles (unverified).
**What the interviewer is checking:** That you know consent and purpose limits exist and will work within them, not that you quote legal sections.
**Say this in the interview:** "As I understand it, we need clear consent for the specific purpose before using someone's data for marketing, we should collect only what we need, and people can withdraw consent. I would confirm details with compliance."
**Explain simply:**
- The **DPDP Act** (Digital Personal Data Protection Act, 2023) is India's law on handling personal data. Details below are from memory, unverified; rules and dates have been phased in and sources conflict, so confirm the current position with the legal team.
- Practical points as I understand them:
  - **Consent** should be free, specific, informed and clear, asked in plain language, for a stated purpose.
  - **Purpose limitation:** data collected for delivering an order should not be reused for marketing without suitable consent.
  - **Data minimisation:** collect and keep only what is needed, and not forever.
  - People can withdraw consent, ask for correction or erasure, and make complaints. Withdrawal should be as easy as giving it.
  - Companies handling data (called data fiduciaries) must keep it secure, and there can be penalties for failures.
- For analysts: store consent status and date with the customer record, respect it in every list, and know what purpose each dataset can be used for.
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the compliance/legal team. This is not legal advice.
**Likely follow-ups:** 1) *Does this replace the SMS rules?* No, as I understand it these are separate regimes that both apply. 2) *What do you change in your work?* Add consent columns, exclude non-consented people, and limit access to personal data.
**Common mistakes:** Assuming "we already have their data" means free use; quoting penalty amounts or dates with confidence; hiding consent status in a separate file nobody joins.

### Q62 ⭐⭐ 🟡 In plain words, what are TRAI's DND (do-not-disturb) and DLT template rules for promotional SMS, and how do they affect campaign reporting? (from memory, awareness level)
**Asked at:** commonly asked (no company-specific report found); relevant to Indian SMS and telecom-based marketing roles (unverified).
**What the interviewer is checking:** Whether you know that regulation changes who you can message and what the delivery data means.
**Say this in the interview:** "As I understand it, promotional SMS must go only to people not on the do-not-disturb list unless they consented, and the sender and message template must be pre-registered. That means some messages are blocked, and reports must separate blocked from delivered."
**Explain simply:** (all from memory, unverified; confirm with compliance and the SMS vendor)
- **TRAI** is the telecom regulator. **DND** (also called the do-not-disturb or do-not-call registry) is a list of numbers whose owners chose not to get promotional calls and messages, in some cases by category.
- **DLT** (distributed ledger technology) is the system telecom operators use to register senders, message templates and consent. As I understand it, a promotional SMS must come from a registered sender ID using an approved template; messages that do not match a template are blocked.
- Transactional or service messages (OTP, order updates) have different treatment from promotional ones.
- **Effect on reporting:**
  - Funnel for SMS: list size, minus DND or no-consent removed, minus rejected (template mismatch), minus failed delivery, equals delivered, then clicks and conversions.
  - Delivery rate and click rate depend on which denominator you use (sent or delivered); state it.
  - Do not read low response as bad creative if many messages never reached anyone.
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the compliance/legal team. Not legal advice.
**Likely follow-ups:** 1) *How do you report blocked messages?* As separate status counts from the vendor delivery report. 2) *Is DND the same as DPDP consent?* No; they are separate rules and a number can pass one and fail the other.
**Common mistakes:** Treating "sent" as "delivered"; comparing SMS campaigns with different template approvals; ignoring the DND filter when estimating reach.

### Q63 ⭐⭐ 🟡 Which fields in a marketing dataset are personal data, and how should an analyst handle them (masking, hashing, access) when sharing files or uploading audiences to an ad platform?
**Asked at:** commonly asked (no company-specific report found); data handling practice is expected in CRM and marketing analyst roles (unverified).
**What the interviewer is checking:** That you recognise personal data, share only what is needed, and know masking from hashing.
**Say this in the interview:** "Name, phone, email, address, device and cookie IDs and anything that can identify a person are personal data. I share the minimum, mask or hash what I can, restrict access, and upload to ad platforms only consented, hashed lists."
**Explain simply:**
- **Personal data** is any information that can identify a person directly or when combined: name, phone, email, address, customer ID, IP address, device or advertising ID, location, even age plus pincode plus job in a small group. Some data is more sensitive (health, finance, children's data); handle with extra care.
- **Masking:** hiding part of a value for display (XXXXXX3210). It is for reading, not matching.
- **Hashing:** turning a value into a fixed scrambled code with a one-way function; the same input always gives the same code, so two files can be matched without showing the raw value. Ad platforms usually ask for hashed email or phone (from memory, check the platform instructions). Hashing is not full anonymity, because common emails can be guessed and hashed again.
- **Access:** share only the needed columns and rows, use role-based access, keep files out of email and personal drives, and set an expiry.
**Worked example:** (pandas, run on invented rows)
```python
import hashlib, pandas as pd
def hash_email(x): return hashlib.sha256(x.strip().lower().encode()).hexdigest()  # clean first, so matches work
df["email_hash"] = df["email"].map(hash_email)
df["phone_masked"] = df["phone"].str.replace(r"\D", "", regex=True).str[-10:].map(lambda p: "XXXXXX" + p[-4:])
```
Output (first 12 characters of hash shown): `ea4e36a82998...` and `10571c2886aa...`; phones `XXXXXX3210` and `XXXXXX6789`. Note " Asha@Example.com" was trimmed and lower-cased before hashing; without that, the same email would hash differently and fail to match.
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the compliance/legal team: consent and purpose limits apply to uploading audiences too.
**Likely follow-ups:** 1) *Is hashed data safe to share freely?* No, it is still personal data in practice. 2) *Why remove columns?* Less data means less to leak.
**Common mistakes:** Hashing without normalising; sharing full files "just in case"; treating masking as protection for data that is later joined back.

### Q64 ⭐⭐ 🟡 Why must opted-out and non-consented customers be excluded from campaign lists and segments, and how would you check your list before it goes out?
**Asked at:** commonly asked (no company-specific report found); list hygiene is a standard CRM and campaign operations task (unverified).
**What the interviewer is checking:** Whether you see exclusion as a legal and trust issue, and whether you have a repeatable pre-send check.
**Say this in the interview:** "Messaging people who opted out or never agreed breaks the law as I understand it, harms trust and hurts email and SMS deliverability. Before sending I match the list against the latest suppression and consent data and reconcile counts."
**Explain simply:**
- **Opt-out** (unsubscribe) means the person asked not to be contacted; **consent** means they agreed to marketing on that channel for that purpose. Both are per channel: email consent is not SMS consent.
- Why it matters: legal risk and penalties (details from memory, unverified, confirm with compliance), complaints and spam flags that damage sender reputation, and brand trust. Also counted results become unreliable if non-consented people are in the base.
- **Pre-send checklist:**
  - Start from the consent flag for the right channel and purpose, with date and source.
  - Exclude the suppression list (unsubscribes, DND, bounced, complaints, recently contacted).
  - Refresh: opt-outs may have arrived since the list was built, so run the check on send day.
  - Reconcile counts: raw list minus each exclusion equals final list, with a number for each step.
  - Check for duplicates and test addresses; sample a few records; keep a log of who approved.
- For segments, apply the same filter before sizing, so reach estimates are real.
**Regulation / privacy note (awareness only):** From memory, unverified, confirm with the compliance/legal team.
**Likely follow-ups:** 1) *Where do you keep the suppression list?* One central table used by every campaign tool. 2) *What if a customer opts out after the list is built?* They must be removed before send; build the check into the process.
**Common mistakes:** Checking consent once at sign-up only; suppression lists per tool that fall out of sync; reporting a campaign's reach before exclusions.

### Q65 ⭐⭐ 🟡 How do cookie consent banners and browser tracking limits change what you can measure in marketing attribution?
**Asked at:** commonly asked (no company-specific report found); cookie-restricted attribution appears in prep-site marketing analyst guides (unverified).
**What the interviewer is checking:** Whether you know that tracking data is now incomplete and biased, and how you adjust.
**Say this in the interview:** "Consent banners and browser limits mean part of the journey is invisible, so tracked conversions undercount reality. I treat platform numbers as a partial view and cross-check with first-party data and incrementality tests."
**Explain simply:**
- **Cookie:** a small file a website stores in your browser so it can recognise you on the next visit. Attribution (giving credit to the ad or channel that led to a sale) relies on it to connect an ad click to a later purchase.
- **Consent banner:** the pop-up asking visitors to accept or reject tracking. Every visitor who rejects is missing from analytics, and they may behave differently from those who accept, so the tracked group is not a random sample.
- **Browser limits:** some browsers (Safari, Firefox) shorten cookie life or block third-party cookies (set by other companies, such as ad networks). A customer who clicks an ad and buys 10 days later may be counted as a new, unattributed visitor. Details change often (from memory, unverified).
- **What you can still measure:** orders in your own system (first-party data, which you collect directly), coupon codes, "how did you hear about us" answers, and total sales before and after a campaign.
- Report conversions as "tracked" versus "total orders", and show the gap.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team: India's data protection law (DPDP Act) is built around consent for a stated purpose; the exact rules for cookies are not something to state from memory.
**Likely follow-ups:** 1) *How do you fill the gap?* Geo or time-based holdout tests and marketing mix modelling (a statistical model on total spend and total sales). 2) *Are modelled conversions fine?* Useful, but they are estimates; label them.
**Common mistakes:** Treating tracked conversions as all conversions; comparing periods before and after a banner change without noting the break; assuming non-consenting visitors behave like consenting ones.

### Q66 ⭐⭐ 🔴 Win rate for one sales region fell from 28% to 19% in a quarter. Walk through your analysis.
**Asked at:** commonly asked (no company-specific report found); win-rate drop diagnosis is a frequent theme in sales analyst prep guides (unverified).
**What the interviewer is checking:** Whether you follow a structured diagnosis: define, check data, split by segment, then look for causes.
**Say this in the interview:** "First I confirm the definition and the data, then I split the drop by deal size, product, rep, source and stage to see whether it is mix or a real fall in performance. Only then do I talk to sales about causes."
**Explain simply:**
- **Win rate:** deals won divided by deals closed (won plus lost) in the period. Definitions differ; some firms divide by all opportunities created, so state yours.
- **Step 1, data:** did the CRM (customer relationship management system) change stage rules, or were many old deals bulk-closed as lost?
- **Step 2, mix versus rate:** did the type of deals change, or did we lose more of the same type?
- **Step 3, drill down:** by rep (new hires?), lead source, competitor named in lost reason, deal size, product, stage where deals die.
- **Step 4, external:** pricing change, new competitor, a big customer segment slowing down.
**Worked example:** (illustrative data, computed by script; 200 closed deals each quarter)

| Segment | Before: closed / won / rate | After: closed / won / rate |
|---|---|---|
| Small deals | 120 / 42 / 35.0% | 80 / 28 / 35.0% |
| Large deals | 80 / 14 / 17.5% | 120 / 10 / 8.3% |
| Total | 200 / 56 / 28.0% | 200 / 38 / 19.0% |

If the mix had changed but each segment's rate stayed the same, the win rate would be 24.5%: a mix effect of 3.5 percentage points. The remaining 5.5 percentage points (24.5% to 19.0%) is a real fall, all in large deals. So the story is "we got more large deals and lost many of them", not "everything got worse".
**Likely follow-ups:** 1) *What if numbers of deals are tiny?* Say the drop may be noise; use a longer window. 2) *What would you recommend?* Review lost-deal reasons for large deals and check whether discounting or approval delays changed.
**Common mistakes:** Jumping to "the team is weak"; not checking the definition; reporting percentage points as percent (28% to 19% is 9 points, a 32% relative fall).

### Q67 ⭐⭐ 🔴 Google Analytics, the ad platforms and the CRM each give different credit to channels, and the CMO asks which channel to cut. How do you advise?
**Asked at:** commonly asked (no company-specific report found); conflicting attribution sources appear in marketing analyst prep guides (unverified).
**What the interviewer is checking:** Whether you avoid trusting one tool blindly and recommend a decision with a test, not just a number.
**Say this in the interview:** "I would not cut a channel based on any single tool. I reconcile the three views, then run a small holdout test on the candidate channel and decide on incremental sales and margin."
**Explain simply:**
- **Why they differ:** each tool uses its own rule. Ad platforms credit themselves for any click or view in a long window; Google Analytics (web analytics) usually credits the last click; the CRM sees the final sale and its revenue but may only record the first lead source.
- **Reconcile first:** compare total conversions against actual orders. The sum of platform claims often exceeds real sales because each takes credit for the same customer.
- **What matters:** incremental sales, meaning sales that would not have happened without the channel, not credited sales. Brand search and retargeting look great but often capture people who would have bought anyway.
- **Advise:** rank channels by cost per incremental order and margin; pause or reduce spend in a test region and watch total sales there against a control region.
- Present a range, not one precise answer, and state assumptions.
**Likely follow-ups:** 1) *No time to test?* Cut the smallest amount from the channel with weakest evidence and watch. 2) *Which source for revenue?* The CRM or finance data, since money is recorded there.
**Common mistakes:** Picking the tool that looks best; ignoring assisted or brand effects; cutting a channel that feeds the others.

### Q68 ⭐⭐ 🔴 Design a customer segmentation for a fintech or e-commerce app: which variables, how many segments, and how would the business use them?
**Asked at:** commonly asked (no company-specific report found); segmentation by purchase history and RFM is common in prep material (unverified).
**What the interviewer is checking:** Whether you tie segments to actions, not just clustering.
**Say this in the interview:** "I would start with simple behaviour-based segments using recency, frequency and spend, with about 4 to 6 groups, each linked to a different action. I would only move to clustering if the simple version misses something."
**Explain simply:**
- **Variables for e-commerce:** days since last order (recency), orders in last 12 months (frequency), total spend (monetary), categories bought, discount reliance, return rate, app or web, city tier.
- **Variables for fintech:** transactions per month, balance or amount transacted, products held (wallet, loan, investment), days since last activity, repayment behaviour.
- **How many:** enough to act on differently. Typical: champions, loyal, new, at risk, lapsed. If a segment has no distinct action, merge it.
- **Uses:** retention offers for at-risk customers, early loyalty perks for champions, onboarding nudges for new users, reduced spend on lapsed customers.
- **Quality checks:** segments should be stable month to month, big enough to measure, and different in outcome (repeat rate, margin).
- Use only data the customer consented to be used for that purpose.
**Likely follow-ups:** 1) *RFM or clustering?* RFM is explainable; clustering (k-means) can find hidden groups but is harder to explain. 2) *How do you test value?* Send different treatments and compare to a holdout.
**Common mistakes:** Creating 15 segments nobody can act on; segmenting only on revenue; never refreshing segments.

### Q69 ⭐⭐ 🔴 A 20% discount on one shampoo brand lifted its units, but a sister brand's units fell. How do you measure cannibalisation and the net result?
**Asked at:** commonly asked (no company-specific report found); uplift versus baseline and cannibalisation are common promotion-analysis themes (unverified).
**What the interviewer is checking:** Whether you compare against a baseline and judge profit, not just units.
**Say this in the interview:** "I estimate what each brand would have sold without the promotion, then compare actual units. Cannibalisation is the sister brand's lost units as a share of the promoted brand's gain, and the net result is total profit across both brands."
**Explain simply:**
- **Baseline:** expected sales without the promotion, from earlier weeks, same weeks last year, or non-promoted stores.
- **Uplift:** actual minus baseline for the promoted brand.
- **Cannibalisation:** sales taken from your own other products. Also check for pull-forward (customers stocked up, so later weeks dip).
- **Net:** add up both brands, and use margin per unit, because the discount lowers margin on every unit sold.
**Worked example:** (illustrative data, computed by script) Brand A: baseline 1,000 units, promo 1,600 units; price Rs 100, unit cost Rs 60, so margin Rs 40 normally and Rs 20 at 20% off. Brand B: baseline 800, actual 600; margin Rs 35 per unit.
- Uplift A: +600 units. Loss B: -200 units. Cannibalisation = 200 / 600 = 33%.
- Net units: +400.
- Profit A: Rs 40,000 to Rs 32,000 (-Rs 8,000). Profit B: Rs 28,000 to Rs 21,000 (-Rs 7,000).
- Net profit: **-Rs 15,000**, even though units rose. Brand A alone would need 2,000 units (double) just to match its old profit.
**Likely follow-ups:** 1) *What else?* Post-promotion dip and competitor brands' effect. 2) *How to get a clean baseline?* A control group of similar stores with no promotion.
**Common mistakes:** Counting only the promoted brand's units; ignoring lower margin; using last week as baseline when seasonality exists.

### Q70 ⭐⭐ 🔴 An email newsletter's open rate jumped from 22% to 60% overnight. What do you check before telling the team it is a success?
**Asked at:** commonly asked (no company-specific report found); metric-spike sanity checks are a frequent case type (unverified).
**What the interviewer is checking:** Whether you doubt a too-good number and check measurement before celebrating.
**Say this in the interview:** "A jump that big overnight is more likely a measurement change than a behaviour change. I would check how opens are counted, what changed in the send, and look at clicks and conversions, which are harder to fake."
**Explain simply:**
- **Open rate:** emails opened divided by emails delivered. An open is usually recorded when a tiny hidden image loads.
- **Machine opens:** some mail apps preload images automatically, so an "open" is recorded even if no human read it. Apple's mail privacy feature does this (from memory, unverified). Security scanners can do the same.
- **Check list:** did the email platform change its counting? Did the share of Apple Mail users change? Did the list shrink after cleaning, changing the denominator? Was it a different subject line, send time or list segment?
- **Confirm with harder signals:** click rate, website visits from the email, orders. If opens tripled but clicks are flat, it is not a success.
- Compare against a prior send to the same segment.
**Likely follow-ups:** 1) *What metric do you trust?* Click-to-open and conversion. 2) *Was the list cleaned?* If inactive subscribers were removed, rates rise without real improvement.
**Common mistakes:** Announcing success from opens alone; ignoring denominator changes; not checking when the change started.

### Q71 ⭐⭐ 🔴 What would you put on a sales performance dashboard for a regional sales head, and what would you leave out?
**Asked at:** commonly asked (no company-specific report found); building a sales dashboard is a common sales analyst theme (unverified).
**What the interviewer is checking:** Whether you design for the user's decisions and keep it focused.
**Say this in the interview:** "I would show attainment against target, pipeline coverage, win rate, deal size and cycle length, plus a list of deals and reps needing attention. I would leave out vanity numbers and detail the head cannot act on."
**Explain simply:**
- **Top row:** revenue versus target (quota attainment), forecast for the quarter, gap to target.
- **Pipeline:** pipeline coverage (open pipeline value divided by remaining target; a rule of thumb is about 3 times, from memory, varies by firm), new pipeline created, stage conversion.
- **Quality:** win rate, average deal size, sales cycle length, discount level.
- **People:** attainment by rep and by team, ramp status for new hires.
- **Action list:** deals stuck too long, large deals closing soon, reps below 50% of target.
- **Leave out:** raw activity counts alone (calls made), all-time totals, ten chart types, anything without a comparison to target or last period.
- Define each metric on the dashboard and show the data refresh date.
**Likely follow-ups:** 1) *How do you decide?* Ask what decisions the head makes weekly. 2) *Filters?* Product, segment, rep, period.
**Common mistakes:** Too many charts; no targets for comparison; mixing bookings and revenue without labels.

### Q72 ⭐⭐ 🔴 The company can add Rs 10 lakh to its marketing budget. How would you use data to decide where it goes?
**Asked at:** commonly asked (no company-specific report found); budget allocation and scale-or-pause decisions appear in prep guides (unverified).
**What the interviewer is checking:** Whether you think in marginal returns (the next rupee), not average returns.
**Say this in the interview:** "I would look at the marginal return of each channel, meaning what the next rupee earns, not the average. I would add the money in stages, starting with channels that still have room and proven incrementality, and measure each stage."
**Explain simply:**
- **Average ROAS** (return on ad spend: revenue divided by spend) can look great because past spend was well targeted; extra spend reaches less interested people, so the **marginal ROAS** is lower.
- **Illustrative example:** Search average 5.0, marginal 1.8 (saturated); Email average 9.0, marginal 0.5 (list is limited); Social average 3.0, marginal 2.5; Video average 2.0, marginal 2.2. The best place for the next lakh is Social or Video, not Search or Email, despite their averages.
- Convert to profit: marginal ROAS must beat the break-even (one divided by the gross margin rate).
- Allocate in tranches (say Rs 2 lakh at a time), keep a holdout, and stop when marginal return reaches break-even.
- Keep a small share for a test of a new channel.
**Likely follow-ups:** 1) *How do you estimate marginal returns?* Past spend-versus-sales variation, geo tests, or a response curve. 2) *Seasonality?* Compare to the same period.
**Common mistakes:** Funding the channel with the highest average ROAS; spending all at once; ignoring margin.

### Q73 ⭐⭐ 🔴 How would you analyse a Diwali campaign fairly against last year's, given different dates, budgets and product ranges?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you align the comparison window and normalise for budget and range.
**Say this in the interview:** "I would line up both years by days relative to Diwali, compare like-for-like products, and judge efficiency per rupee spent, not total revenue alone."
**Explain simply:**
- **Dates:** Diwali moves each year (from memory, it fell in early November in 2024 and in October in 2025; unverified). Compare "day minus 21 to day plus 7" around the festival, not calendar dates.
- **Budget:** compare revenue per rupee spent (ROAS) and also the incremental revenue per extra rupee.
- **Product range:** compare only products sold in both years for the like-for-like view; report new products separately.
- **Baseline:** also compare each year to its own normal weeks, so growth of the whole business is not credited to the campaign.
- **Worked example:** (illustrative, computed by script) Last year revenue Rs 400 lakh on spend Rs 40 lakh (ROAS 10.0). This year Rs 500 lakh on Rs 60 lakh (ROAS 8.3). Revenue rose by Rs 100 lakh for Rs 20 lakh extra, so the extra spend returned 5.0 per rupee. Total looks better; efficiency is lower; the extra rupee still earns.
**Likely follow-ups:** 1) *Other differences?* Competitor activity and the economy. 2) *Margin?* Check discount depth each year.
**Common mistakes:** Comparing calendar dates; comparing total revenue with a bigger budget; including products that did not exist last year.

### Q74 ⭐⭐ 🔴 A sales team's attrition doubled this year. How would you estimate the effect on pipeline, quota attainment and revenue, and what data would you pull from the HR system and the CRM?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question tied to HR and sales analytics.
**What the interviewer is checking:** Whether you can connect people data to revenue, a strong point for an HR-background candidate.
**Say this in the interview:** "Each leaver costs a vacancy period and a ramp-up period. I would estimate lost productive months per leaver, multiply by extra leavers, and convert to revenue using typical output per rep."
**Explain simply:**
- **Quota:** the sales target given to a rep. **Ramp:** the months a new hire needs to reach full productivity.
- **Pipeline impact:** a leaver's open deals are reassigned, often slowing or being lost.
- **Worked example:** (illustrative, computed by script) 50 reps; attrition 15% to 30%, so 7.5 extra leavers. Vacancy 2 months, ramp 4 months at 50% productivity (so 2 months lost): 4 months lost per leaver. Lost rep-months = 7.5 x 4 = 30, which is 5% of capacity (30 of 600 rep-months). At Rs 10 lakh per rep-month, about Rs 300 lakh (Rs 3 crore) of capacity at risk.
- That is a ceiling; managers may cover territories, so compare with actual results.
**Data and tables involved:** HR: employee id, hire date, exit date, role, manager, territory, exit reason, salary band. CRM: opportunities (owner, amount, stage, created and close dates), quota table (rep, period, target), activity. First cuts: attainment by tenure band, deals lost or reassigned after an owner left, and territory coverage gaps.
**Regulation / privacy note (awareness only):** employee data is personal data; use only what is needed, restrict access, and report in aggregate (from memory, unverified, confirm with HR and legal).
**Likely follow-ups:** 1) *Which exits matter most?* Top performers. 2) *Cost to replace?* Recruitment, training and lost sales.
**Common mistakes:** Ignoring ramp time; using company-wide attrition rather than sales; assuming every leaver was an average performer.

### Q75 ⭐⭐ 🔴 A B2B company's sales cycle lengthened from 60 to 90 days. What could be the causes and how would you split them with data?
**Asked at:** commonly asked (no company-specific report found); cycle length is a standard sales analytics metric (unverified).
**What the interviewer is checking:** Whether you decompose a total into stages and separate mix from real slowdown.
**Say this in the interview:** "I would break the 90 days by stage to see where the extra 30 days sits, then check whether deal mix changed, and finally look at reasons such as buyer approvals or process changes."
**Explain simply:**
- **Sales cycle:** days from opportunity created to closed-won (won deals only, or say otherwise).
- **Mix causes:** more large or enterprise deals, which naturally take longer.
- **Real causes:** longer buyer approvals (legal, procurement), new competitors, weaker leads, a slow internal quote or discount approval, new reps.
- **Worked example:** (illustrative, computed by script) Stage days before to after: qualification 10 to 12; demo 15 to 18; proposal 15 to 20; negotiation 12 to 15; legal and procurement 8 to 25. Total 60 to 90. Of the 30 extra days, 17 are in legal and procurement, so that is the first thing to investigate.
- Split by deal size, segment, rep and source to separate mix from stage delays; also watch whether the data includes deals still open: deals that have not closed yet are missing from the average, which makes recent cycles look shorter than they will turn out.
**Likely follow-ups:** 1) *Won only?* Include lost deals too, since slow deals may be dying. 2) *Action?* Standard contract templates, earlier legal involvement.
**Common mistakes:** Quoting only the average; ignoring mix; comparing quarters with different closing patterns.

### Q76 ⭐⭐ 🔴 Customers who got a discount coupon in their first order have lower repeat rates than those who did not. How do you interpret this?
**Asked at:** commonly asked (no company-specific report found); a standard correlation-versus-causation case.
**What the interviewer is checking:** Whether you see selection bias and avoid concluding that coupons cause low repeat.
**Say this in the interview:** "This is a correlation. Coupons may attract bargain hunters who would not return anyway, or be given to riskier customers. I would compare similar customers or use a randomised test before judging the coupon."
**Explain simply:**
- **Selection bias:** the coupon group was not chosen at random. They may come from a different channel, product or city, or be deal-seekers.
- **Possible explanations:** coupon customers are price-sensitive; they were acquired through aggressive campaigns; the coupon pulled a purchase forward; or the coupon really does attract low-quality customers.
- **How to check:** compare within the same channel, category and order value; or use a past test where coupons were randomly given; or run a new test with a holdout group.
- **Measure properly:** repeat rate within 60 or 90 days, plus margin, because a coupon customer who repeats may still be less profitable.
**Likely follow-ups:** 1) *Can coupons still be worth it?* Yes, if lifetime profit exceeds cost. 2) *Matching?* Pair customers with similar attributes.
**Common mistakes:** Concluding "stop coupons"; not controlling for channel; comparing short windows for customers acquired at different times.

### Q77 ⭐⭐ 🔴 A segment called 'high-value customers' is built on last year's revenue only. What problems can this cause and how would you improve it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you see that past revenue is a poor and one-dimensional proxy for future value.
**Say this in the interview:** "Last year's revenue rewards one-off big spends and ignores recency, margin and future potential. I would combine recency, frequency, margin and predicted future value."
**Explain simply:**
- **Problems:** a one-time bulk buyer looks high-value but may never return; a loyal customer who joined late last year looks small; customers who are about to leave still qualify; heavy discount users count despite low margin; returns may not be netted off.
- **Improvements:** use revenue net of returns; use margin or profit; add recency and frequency (RFM); use a longer window with weights; add a predicted next-12-month value from a simple model; refresh regularly.
- **Check:** compare how well each definition predicts next year's profit.
- Keep the label and the definition written down, so teams do not treat it as a fixed truth.
**Likely follow-ups:** 1) *Simple fix?* Add recency and net margin. 2) *How often to refresh?* Monthly or quarterly.
**Common mistakes:** Treating revenue as value; never refreshing; using a rigid threshold that flips customers in and out.

### Q78 ⭐ 🟢 What is a customer data platform (CDP), a 'customer 360' view and identity resolution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the vocabulary and why combining data matters.
**Say this in the interview:** "A CDP collects customer data from many systems into one place, a customer 360 is the single combined profile of each person, and identity resolution is the matching that decides which records belong to the same person."
**Explain simply:**
- **CDP:** software that gathers data from the website, app, CRM, store and email, and makes unified profiles available to marketing tools.
- **Customer 360:** one view of a customer: purchases, visits, support tickets, preferences.
- **Identity resolution:** matching records, for example a phone number from the app, an email from newsletters and a loyalty card in store, into one customer. Matching can be exact (same phone) or fuzzy (similar name and address).
- Think of an HR system where one employee has different ids in payroll, attendance and training; matching them is the same problem.
**Regulation / privacy note (awareness only):** unified profiles raise privacy risks; consent and purpose limits matter (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Risk of wrong matches?* Merging two people shows one person's data to another. 2) *Is a CDP a warehouse?* No; it is built for profiles and activation.
**Common mistakes:** Assuming matching is perfect; ignoring consent; confusing CDP and CRM.

### Q79 ⭐ 🟢 What is account-based marketing (ABM), and which metrics differ from a normal lead-based approach?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand targeting companies, not individuals, and measure accordingly.
**Say this in the interview:** "ABM targets a chosen list of companies with tailored campaigns. Metrics shift from lead counts to account engagement, buying-committee coverage, pipeline and revenue per account."
**Explain simply:**
- **Lead-based:** attract many individuals, score them, hand good ones to sales. Metrics: leads, MQLs (marketing qualified leads), cost per lead.
- **ABM:** sales and marketing pick target accounts first, then reach several people at each company (the buying committee).
- **ABM metrics:** account engagement score, share of target accounts engaged, number of contacts reached per account, accounts moving to opportunity, pipeline and revenue from target accounts, deal size, cycle length.
- It suits expensive deals with few buyers, where one account is worth a lot.
**Likely follow-ups:** 1) *Do leads still matter?* Less; one engaged account can matter more. 2) *Cost?* Higher per account, so ROI is measured per account.
**Common mistakes:** Measuring ABM by lead volume; not agreeing the account list with sales.

### Q80 ⭐ 🟢 What is the difference between SEO and SEM, and what does an analyst measure for each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the basics of free versus paid search.
**Say this in the interview:** "SEO is earning a higher place in unpaid search results; SEM here means paying for search ads. SEO is measured by organic traffic and rankings, SEM by clicks, cost and conversions."
**Explain simply:**
- **SEO (search engine optimisation):** improving a site so it ranks higher in unpaid results. Results are slow and spend is mostly effort.
- **SEM (search engine marketing):** buying ad placement on search results; traffic is quick and stops when spend stops. Some people use SEM to mean both; state your meaning.
- **SEO metrics:** organic sessions, keyword rankings, click-through rate from results, pages indexed, conversions from organic visits.
- **SEM metrics:** impressions, clicks, CTR (click-through rate), CPC (cost per click), conversion rate, cost per acquisition, ROAS.
- Brand and non-brand keywords should be tracked separately.
**Likely follow-ups:** 1) *Which is better?* They complement; SEM for fast results, SEO for lasting traffic. 2) *Overlap?* Paid ads on keywords you already rank for may be wasted spend; test.
**Common mistakes:** Counting brand searches as SEO success; ignoring conversions and judging only by traffic.

### Q81 ⭐ 🟢 What is a sales and marketing service-level agreement (SLA), and what metrics show whether the lead handoff works?
**Asked at:** commonly asked (no company-specific report found); lead handoff and MQL/SQL definitions appear in prep-site marketing and sales analyst guides (unverified).
**What the interviewer is checking:** That you know marketing and sales must agree in writing on lead quality and follow-up speed, and that you can measure it.
**Say this in the interview:** "A sales and marketing SLA is a two-way promise: marketing delivers leads that meet an agreed definition, and sales follows up within an agreed time. I would check it with acceptance rate, speed to first contact, and how many handed-over leads become opportunities."
**Explain simply:**
- A **lead** is a person or company who showed interest. A **marketing qualified lead (MQL)** passes marketing's score or rules; a **sales qualified lead (SQL)** is one a salesperson has accepted as worth pursuing. Exact definitions differ by company.
- Marketing's side: volume and quality of MQLs. Sales' side: contact within, say, 24 hours and a recorded outcome (accepted or rejected with a reason).
- Think of it like HR and a hiring manager agreeing on a candidate profile and a 48-hour feedback time.
**Worked example:** 1,000 MQLs handed over; 600 accepted (60% acceptance); 450 reached an opportunity stage (75% of accepted); 54 won (12% of opportunities). Low acceptance points to a quality or definition gap; slow contact points to a sales follow-up gap.
**Likely follow-ups:** 1) *Which metric first?* Acceptance rate and rejection reasons. 2) *What if sales ignores leads?* Report speed to first contact and untouched leads by owner.
**Common mistakes:** Counting leads only by volume; no rejection reasons captured; reporting to one team instead of both.

### Q82 ⭐ 🟢 What is marketing mix modelling, and how is it different from attribution?
**Asked at:** commonly asked (no company-specific report found); appears in marketing analytics prep guides (unverified).
**What the interviewer is checking:** Whether you understand top-down versus user-level measurement.
**Say this in the interview:** "Marketing mix modelling (MMM) uses totals over time, such as weekly spend per channel and weekly sales, in a regression (a statistical method that finds how sales move with spend) to estimate how much each channel contributes. Attribution follows individual customer journeys and gives credit to touchpoints."
**Explain simply:**
- **MMM:** top-down; practitioners often say it needs a year or more of weekly data (from memory, unverified); includes things you cannot click on (TV, hoardings, discounts, seasonality, festivals). Needs no personal data.
- **Attribution:** bottom-up, needs tracked clicks or logins per user; blind to offline media and weakened when tracking is restricted.
- MMM answers "how should we split next year's budget?"; attribution answers "which ad or email in the journey should we tweak this week?"
- Analogy: MMM is checking overall headcount cost against output by department; attribution is tracing one employee's path.
**Likely follow-ups:** 1) *Weakness of MMM?* Needs enough spend variation; gives correlation unless backed by experiments. 2) *Can both be used?* Yes; calibrate each against holdout tests.
**Common mistakes:** Treating them as competitors; trusting MMM from only a few months of data; ignoring seasonality.

### Q83 ⭐ 🟢 What are the common brand health metrics (awareness, consideration, share of voice, NPS), and how are they measured?
**Asked at:** commonly asked (no company-specific report found); brand metrics appear in marketing KPI guides from vendors (unverified).
**What the interviewer is checking:** That you know brand measures are mostly survey-based and slow-moving, unlike click metrics.
**Say this in the interview:** "Brand health tracks how people think about us: awareness (do they know us), consideration (would they consider us), share of voice (our share of category advertising or conversation) and NPS (would they recommend us)."
**Explain simply:**
- **Awareness:** survey a sample; "unaided" means they name us unprompted, "aided" means they recognise us from a list.
- **Consideration:** share of respondents who say they would consider buying.
- **Share of voice:** our advertising spend or mentions divided by the category total; from media-tracking or social-listening data.
- **NPS (Net Promoter Score):** ask "how likely to recommend, 0 to 10?"; promoters score 9-10, detractors 0-6; NPS = % promoters minus % detractors.
- Same logic as an employee engagement survey: sample, repeat on a schedule, compare waves.
**Worked example:** 100 respondents: 50 promoters, 30 passives, 20 detractors, so NPS = 50% - 20% = 30 (a score, not a percentage).
**Likely follow-ups:** 1) *Link to sales?* Loosely, over quarters; use trends. 2) *Sample issues?* Small or biased samples; report margin of error.
**Common mistakes:** Quoting NPS as a percentage; comparing waves with different sample mix; expecting weekly movement.

### Q84 ⭐ 🟢 What are the sales forecast categories (commit, best case, pipeline), and how do sales teams use them?
**Asked at:** commonly asked (no company-specific report found); forecasting categories appear in sales-ops prep guides (unverified).
**What the interviewer is checking:** That you know how deals are bucketed by confidence and how a forecast is built from the buckets.
**Say this in the interview:** "Commit is deals the rep is confident will close this period, best case adds deals that could close with some luck, and pipeline is everything open. Teams add commit to closed deals for a floor, and use best case as upside."
**Explain simply:**
- **Closed won:** already signed. **Commit:** rep stakes their name on it. **Best case:** possible but with risks. **Pipeline:** all open opportunities, early ones included.
- Category names and rules vary by company; reps' labels are judgement, so analysts test them against history.
- Analogy: offers accepted, offers in negotiation, and candidates still interviewing.
**Worked example:** Rs lakh, treating the three buckets as separate, not overlapping: commit 120, best case 200, pipeline 400. With historical win rates 90%, 40%, 10% (invented): 108 + 80 + 40 = 228 lakh expected on top of closed deals.
**Likely follow-ups:** 1) *Are rep labels reliable?* Check commit-to-actual accuracy per rep. 2) *Weighted or not?* Show both.
**Common mistakes:** Adding all pipeline at face value; counting commit twice inside best case; not freezing the forecast at period start to measure accuracy.

### Q85 ⭐ 🟢 What is pipeline velocity, and which four things move it?
**Asked at:** commonly asked (no company-specific report found); velocity appears in sales analyst prep guides (unverified).
**What the interviewer is checking:** Whether you can state the formula and use it to find levers.
**Say this in the interview:** "Pipeline velocity is how much revenue the pipeline produces per day: number of opportunities times win rate times average deal size, divided by sales cycle length in days."
**Explain simply:**
- Four levers: more opportunities, higher win rate, bigger deals, shorter cycle. (An **opportunity** is a live sales deal; **sales cycle** is days from creation to close.)
- Improving any one raises velocity; the formula shows which lever is cheapest.
**Worked example:** 40 opportunities x 25% x Rs 8 lakh / 80 days = Rs 1.0 lakh per day.
- 50 opportunities: 1.25. Win rate 30%: 1.20. Deal size Rs 10 lakh: 1.25. Cycle 60 days: 1.33.
- Shortening the cycle by 20 days gives the biggest gain here.
**Likely follow-ups:** 1) *Use?* Compare teams or quarters. 2) *Limits?* Averages hide spread; use closed deals for win rate and cycle.
**Common mistakes:** Mixing deal sizes across products; counting open deals in win rate; forgetting units.

### Q86 ⭐ 🟡 A sales rep leaves and a new rep takes a quota of Rs 60 lakh a quarter with a three-month ramp (25%, 50%, 100% of quota in the three months). What is the quota capacity lost in the first quarter, and why should the HR and sales-ops teams plan for it?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured gap-fill, not tied to a reported interview.
**What the interviewer is checking:** Simple arithmetic and whether you link attrition to revenue capacity.
**Say this in the interview:** "A quota is a sales target. Spreading Rs 60 lakh evenly gives Rs 20 lakh a month; the new rep delivers 5, 10 and 20, so 35 lakh of 60. About Rs 25 lakh, or 42%, of capacity is lost, before counting any vacancy time."
**Explain simply:**
- **Ramp** is the period when a new joiner is not yet fully productive. Assumption: the percentages apply to each month's one-third of quota.
- Hiring time also loses capacity: one empty month adds another Rs 20 lakh (total 45 lakh).
- HR plans hiring lead time and onboarding; sales-ops adjusts team targets and forecast so the shortfall is not a surprise.
**Worked example:** Month 1: 20 x 25% = 5. Month 2: 20 x 50% = 10. Month 3: 20 x 100% = 20. Total 35. Lost: 60 - 35 = 25 lakh = 41.7% of quota.
**Likely follow-ups:** 1) *Other cost?* Recruiting, training, lost deals. 2) *Reduce it?* Hire earlier, shadowing, handover of warm accounts.
**Common mistakes:** Applying the ramp percentages to the full Rs 60 lakh; ignoring vacancy time; forgetting the loss recurs per exit.

### Q87 ⭐ 🟡 How would you build a recruitment-marketing funnel (career site visit, application start, application, interview, offer, joined) using web analytics and HR system data, and what are its marketing-style metrics?
**Asked at:** commonly asked (no company-specific report found); a gap-fill linking marketing funnels to talent acquisition.
**What the interviewer is checking:** That you can join two data sources and apply marketing thinking to hiring.
**Say this in the interview:** "The top steps come from web analytics and the later steps from the applicant tracking system (ATS). I would join them using a source tag on the application link and report stage conversion, cost per application and cost per hire by source."
**Explain simply:**
- **Web analytics** (tools such as Google Analytics; from memory, unverified) gives visits and application starts. The **ATS** gives applications, interviews, offers, joined.
- The join: UTM tags (labels on links recording the source, such as a job board) stored with each application. Without them, the funnel breaks at the application step.
- Marketing-style metrics: conversion per step, drop-off, cost per application, cost per hire, source quality (share of applicants who get hired).
- Candidate data is personal data: keep it aggregated and limit access.
**Worked example (invented):** 20,000 visits, 1,200 starts (6.0%), 800 applications (66.7% of starts; 33.3% abandon), 160 interviews (20%), 40 offers (25%), 28 joined (70%). Visit to joined: 0.14%. With Rs 2.8 lakh spend: Rs 350 per application, Rs 10,000 per hire.
**Likely follow-ups:** 1) *Best source?* Compare joined per source, not applications. 2) *Why drop at start?* Long form; test it.
**Common mistakes:** Ranking sources by volume; counting visits as people; no source tag.

### Q88 ⭐ 🟡 In plain words, what is the role of ASCI (the advertising standards body in India) for marketing claims, and when might an analyst be asked for evidence? (from memory, awareness level)
**Asked at:** commonly asked (no company-specific report found); awareness-level question.
**What the interviewer is checking:** That you know ad claims can be challenged and you would keep evidence ready.
**Say this in the interview:** "From memory, unverified: ASCI is a self-regulatory body that reviews ads after complaints against its code, for example misleading claims. If a claim like 'highest rated' or '30% more effective' is questioned, an analyst may be asked for the data behind it."
**Explain simply:**
- Self-regulatory means set up by the industry itself, not a government agency; other laws and regulators also apply (confirm with the legal team).
- Analyst's role: document how each number was computed, the sample, period and comparison.
- Claims needing support: comparisons, "number one", percentage improvements, survey results, testimonials.
- Keep a reproducible record: query, dates, definitions, and caveats.
**Regulation / privacy note (awareness only):** From memory, unverified; confirm with the compliance/legal team. This is not legal advice.
**Likely follow-ups:** 1) *What evidence?* Method, sample, dates, source data. 2) *Who decides?* Legal and compliance, not the analyst.
**Common mistakes:** Cherry-picking a favourable period; no saved method; stating a claim as certain.

### Q89 ⭐ 🔴 How would you forecast next quarter's revenue from the CRM pipeline, and how would you state your confidence to leadership?
**Asked at:** commonly asked (no company-specific report found); forecast accuracy appears in sales analyst guides (unverified).
**What the interviewer is checking:** Evidence-based weighting, honest ranges, and tracking of forecast error.
**Say this in the interview:** "I would take closed revenue so far, add open deals weighted by historical stage win rates, adjust for timing, and give leadership a low, expected and high range instead of one number, then track my error."
**Explain simply:**
- **CRM** is the system where deals are logged. Pull deals with stage, amount, expected close date and age.
- Win rates come from past closed deals by stage and segment, not rep opinion alone.
- Deals slip: use close date history, and exclude stale deals.
- Give a range from scenarios: pessimistic win rates, expected, optimistic.
**Worked example (Rs lakh, invented; the buckets are separate, not overlapping):** Closed 150. Commit 120, best case 200, pipeline 400. Low rates (80%, 20%, 5%): 156, total 306. Expected (90%, 40%, 10%): 228, total 378. High (95%, 50%, 15%): 274, total 424. Say: "Most likely about 378, plausible range 306 to 424."
**Likely follow-ups:** 1) *Check quality?* Compare past forecasts to actuals (error percentage). 2) *Deals slip?* Model close-date slippage.
**Common mistakes:** One precise number; unweighted pipeline; changing the forecast after the fact.

### Q90 ⭐ 🔴 A sales commission plan pays on bookings, not collections. What behaviours and data problems might that create, and what would you report?
**Asked at:** commonly asked (no company-specific report found); an HR and sales-ops gap-fill question.
**What the interviewer is checking:** That you see incentives shape behaviour and can design checks.
**Say this in the interview:** "A booking is a signed order; a collection is money received. Paying on bookings can reward deals that never pay, heavy discounting, or pushing deals into the period. I would report bookings alongside collections, cancellations and overdue receivables by rep."
**Explain simply:**
- Behaviours: aggressive discounts, loose payment terms, signing weak customers, end-of-quarter pulling forward, booking deals that later cancel.
- Data problems: booking date versus invoice date versus payment date; credit notes and cancellations not linked back; split credit between reps; commission paid before clawback.
- Reports: booked-to-collected ratio, days to collect, cancellation or return rate, average discount, commission paid versus cash received.
- Options (a conversation with HR and finance): partial payment on collection, or clawback (recovering commission if the customer cancels or does not pay).
- Compensation data is sensitive; restrict access.
**Likely follow-ups:** 1) *Quarter-end spike?* Check bookings by week. 2) *Fix?* Pay part on collection.
**Common mistakes:** Blaming reps rather than the design; ignoring refunds; comparing reps with different territories.

### Q91 ⭐ 🔴 How would you set up a test to decide between two price points for a subscription product, and what would you watch besides conversion?
**Asked at:** commonly asked (no company-specific report found); pricing tests appear in marketing analytics prep guides (unverified).
**What the interviewer is checking:** Test design and whether you judge revenue and retention, not conversion alone.
**Say this in the interview:** "I would randomly show each new visitor one price, run it for full weekly cycles, and compare revenue per visitor, not just conversion. Then I would follow retention and refunds, because the cheaper plan may attract customers who leave sooner."
**Explain simply:**
- Randomise new visitors (not existing customers), define success and duration before starting, and ensure sample size is enough to detect the difference.
- Watch: revenue per visitor, plan mix, refunds, cancellations after 1-3 months, support tickets, customer complaints about price differences.
- Fairness and legality: showing different prices to different people may upset customers; confirm with legal and product.
**Worked example (invented):** Price A Rs 499 at 4.0% conversion gives Rs 19.96 per visitor; price B Rs 599 at 3.5% gives Rs 20.97, about 5% higher despite lower conversion. B wins only if retention holds.
**Likely follow-ups:** 1) *Stop early?* No, peeking inflates false positives. 2) *Too few visitors?* Test a bigger difference or run longer.
**Common mistakes:** Picking by conversion; ending after a few days; mixing in a promotion.

### Q92 ⭐ 🔴 Marketing wants to credit a webinar for the deals it touched. How do you decide whether the webinar influenced the deals or just met people who were already buying?
**Asked at:** commonly asked (no company-specific report found); attribution scepticism appears in marketing analytics guides (unverified).
**What the interviewer is checking:** Correlation versus causation and selection bias.
**Say this in the interview:** "Attendees are self-selected: people already interested are more likely to attend and buy. I would compare attendees with similar non-attendees, ideally using a holdout, and look at timing and deal speed."
**Explain simply:**
- **Touched** means the contact appeared in the webinar list before the deal closed; it says nothing about cause.
- Check: were the deals already open before the webinar? Compare win rate and cycle length of attendees versus matched non-attendees (same size, industry, stage).
- Best evidence: invite a random half and hold out the rest; compare.
- Report as "associated with" unless a test supports "caused".
**Likely follow-ups:** 1) *No holdout possible?* Use matching and report the caveat. 2) *Fair credit?* Share credit using a stated rule.
**Common mistakes:** Counting deals open before the event; ignoring that registrants differ; claiming causation.

### Q93 ⭐ 🔴 How would you build a simple lead-scoring model for a B2B company, and how would you check it works and is not biased by sales follow-up?
**Asked at:** commonly asked (no company-specific report found); lead scoring appears in B2B marketing analyst guides (unverified).
**What the interviewer is checking:** Modelling basics, validation on unseen data, and awareness of feedback bias.
**Say this in the interview:** "I would use past leads with the outcome 'became a customer', score them with a simple logistic regression or points system on firm and behaviour features, test on later time periods, and check that scores predict wins even among leads that sales contacted equally."
**Explain simply:**
- **B2B** means selling to businesses. Features: company size, industry, job title, pages viewed, emails opened. Outcome: converted within a set time.
- **Logistic regression** gives a probability from 0 to 1; a simple points table is easier to explain.
- Validate on a later period, not random rows; check ranking (are top-decile leads converting most) and calibration (does a 20% score win about 20%).
- Follow-up bias: sales called high-score leads first, so they converted partly because of attention. Compare by contact speed, or hold out a random group from priority treatment.
- Avoid features that proxy for personal traits; review fairness.
**Likely follow-ups:** 1) *Metric?* Conversion by score band, and AUC (a 0.5-to-1 score of how well the model ranks winners above non-winners; 0.5 is a coin toss). 2) *Refresh?* Retrain regularly.
**Common mistakes:** Random split with time leakage; using fields filled after sales contact (leakage); never re-checking.

# Question data for Book 6 Part 9. Tuple: (stars, difficulty, scenario text, asked-key). All numbers are invented illustrative numbers.
import math
NS = "; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened"
AS = {
 'FC': "Fintech and credit-scoring material (a codemia Capital One data scientist guide and Interview Query fintech and lender guides list thin-file features, alternative data, class imbalance, regulatory limits on features and false-positive versus false-negative cost trade-offs; Altair, RiskSpan, SAS and HAL pages describe reject inference); prep and practitioner material rather than a confirmed employer round" + NS,
 'FP': "Payments-fraud material (2025 SciTePress, Atlantis Press and SDMIMD papers and student projects on UPI fraud detection frame false alerts, class imbalance and retraining on confirmed fraud and false-positive reports); academic and self-published material, no interview bank for this exact framing" + NS,
 'EP': "E-commerce ML material (prachub lists Shopify questions on product ranking for a marketplace, package delivery time prediction and personalised product feeds, and a CleverPrep Shopify guide lists search-ranking and embedding trade-offs; Interview Query notes e-commerce promotion and behaviour modelling); candidate-reported and prep-site material" + NS,
 'EF': "Marketplace-trust material (a prachub Amazon fake-review question on detection signals and impact metrics, an Interview Query fake-review prompt and DoorDash and Thumbtack data scientist guides on marketplace analytics); prep-site material and one estimate-based news item, no confirmed employer round" + NS,
 'HE': "Clinical-AI external-validation coverage (Fierce Healthcare, MedCity News and JAMA Internal Medicine pages on the external validation of a widely deployed sepsis model, which reported low sensitivity, a modest positive predictive value, alerts on a large share of patients and a billing-code outcome definition; a newsletter piece on local validation and tracking override patterns); published news and research, not an interview bank" + NS,
 'HD': "Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks" + NS,
 'AC': "Ads ML and calibration material (Dataford questions on CTR calibration and click-through rate at an ad-tech firm, AlgoMaster and Educative ad click prediction system-design pages with calibration-error checks by probability bin); prep-site material" + NS,
 'AP': "Ad-serving system-design material (techinterview.org ad serving and real-time bidding pages, a Dataford question on budget pacing and frequency capping, machinelearningatscale.com on frequency capping; feedback-controller pacing, per-user counters and credits for invalid clicks appear in the snippets); prep-site material" + NS,
 'AI': "Ads measurement material (an eMarketer 2026 FAQ separating incrementality, multi-touch attribution and marketing mix modelling, Google ads-measurement data scientist postings asking for causal inference and attribution work, a Dataford incremental-lift question, a Remerge incrementality write-up); job postings and prep material rather than a confirmed interview round" + NS,
}
ED = "No public page found for this exact scenario, editor-designed; the theme is adjacent to "
Q = []
def add(s, d, t, a):
    if a.startswith('ED:'):
        AS.setdefault(a, ED + a[3:] + "; related topics appear in public guides; no page for the exact framing; search snippets only, not opened")
    Q.append((s, d, t, a))

# ======================= 3 stars, green =======================
# Fintech: single-threshold payments fraud
fr, fl, caught = 1000, 2000, 600
assert fr/1000000 == 0.001 and caught/fl == 0.3 and caught/fr == 0.6
assert (fl-caught)*20 == 28000 and (fr-caught)*500 == 200000 and caught*500 == 300000
add(3, '🟢', "Fintech: A payments app sees 1,000,000 transactions a day, of which 1,000 (0.1% of transactions, a measured monthly average) are fraud. The model blocks 2,000 transactions a day and 600 of the blocked ones are fraud. A blocked genuine customer costs 20 in support and lost goodwill, a missed fraud costs 500 and a caught fraud saves 500. Compute precision, recall and the daily cost of friction versus missed fraud, and say what else you need to know before calling this model good.", 'FP')
# E-commerce: position bias
assert 11/4 == 2.75
add(3, '🟢', "E-commerce: In a search log, results at position 1 get a 12% click-through rate per impression and results at position 5 get 4%, averaged over thousands of queries (measured). A new ranker moves one product from position 5 to position 1 and its click-through rate rises from 4% to 11%. The product manager says the product became 2.75 times more relevant. How do you respond, and how would you estimate relevance separately from position?", 'EP')
# Healthcare: prevalence and PPV
def ppv(prev, n=10000, se=0.90, sp=0.95):
    d = round(n*prev); h = n-d; tp = round(d*se); fp = round(h*(1-sp)); return d, tp, fp, tp/(tp+fp)
assert ppv(0.20) == (2000, 1800, 400, 1800/2200) and abs(ppv(0.20)[3]-0.818) < 0.001
assert ppv(0.01)[:3] == (100, 90, 495) and abs(ppv(0.01)[3]-0.1538) < 0.001
add(3, '🟢', "Healthcare: A screening model has 90% sensitivity and 95% specificity and was validated in a referral hospital where 20% of patients have the condition. It is now deployed in a community clinic where the prevalence is 1% (an assumed planning figure, not measured). For 10,000 patients in each setting, compute the true positives, false positives and positive predictive value, and say how you would explain the difference to clinic staff.", 'HE')
# Ads: calibration and bid
assert 24000/1000000 == 0.024 and abs(0.03*10-0.3) < 1e-12 and abs(0.024*10-0.24) < 1e-12 and abs(0.30/0.24-1.25) < 1e-12
add(3, '🟢', "Ads: A click model predicts an average click-through rate of 3.0% on 1,000,000 impressions, but 24,000 clicks were observed, an observed rate of 2.4% (a measured day). The AUC is unchanged and advertisers bid a value per click of 10, so the bid per impression is the predicted rate times 10. Compute the bid per impression with and without the error and the relative overbid compared with the calibrated bid, and explain why a good AUC does not protect you here and how you would fix it.", 'AC')
# E-commerce: delivery promise
assert 50000-44000 == 6000 and 44000/50000 == 0.88 and round(6000*0.10) == 600 and round(50000*0.03) == 1500
add(3, '🟢', "E-commerce: Checkout shows a delivery promise of 3 days, and in a sample of 50,000 delivered orders 44,000 (88%) arrived within the promise, which leaves 6,000 late orders. Late orders have a 30-day repeat-purchase rate of 20% against 30% for on-time orders (absolute, per customer, measured sample), a gap that is 600 repeat purchases across the 6,000 late orders. A 4-day promise would be met on an assumed 97% of orders, which is 1,500 late orders per 50,000, but checkout conversion might fall. How do you choose the promise, and what experiment would you run?", 'EP')

# ======================= 3 stars, yellow =======================
# F thin-file
assert 2000*5000 == 10000000 and abs(1200/(1200+4000)-0.2308) < 1e-4
add(3, '🟡', "Fintech: A lender gets 100,000 applications a month and 30,000 of them (30% of applications) are thin-file with no bureau score, and its model has an AUC of 0.82 on thick-file applicants but 0.66 on thin-file ones. A pilot would approve 2,000 extra thin-file applicants a month with a credit limit of 5,000 each, a profit of 1,200 per repaying customer and a loss of 4,000 per defaulter. Compute the exposure of the pilot as an upper bound on balances at risk (all limits fully drawn, no recovery) and the break-even default rate, and explain what data, controls and review you would use.", 'FC')
# E cold-start sellers
expl = 10000000*0.05
lost = expl*(0.03-0.02); base = 10000000*0.03
assert expl == 500000 and round(lost) == 5000 and base == 300000 and abs(lost/base-0.01667) < 1e-4
add(3, '🟡', "E-commerce: New sellers make up 8% of live listings but receive 2% of search impressions, because the ranker favours listings with a conversion history. The team wants to reserve 5% of 10,000,000 daily search impressions for exploration, in addition to the 2% they already get, where new listings are assumed to convert at 2.0% per impression against 3.0% for the normal ranking (a projection). Compute the daily orders given up by the exploration budget in absolute and relative terms, and say how you would run the exploration and judge whether it is worth it.", 'ED:cold-start in marketplace search and recommendation system-design material')
# H alarm fatigue
assert 60/80 == 0.75 and 60/600 == 0.1 and 40/80 == 0.5 and 40/100 == 0.4 and abs((60-40)/(600-100)-0.04) < 1e-12
add(3, '🟡', "Healthcare: A ward deterioration model sees 80 real deterioration events a day and nurses can respond to at most 100 alerts a day. At the current threshold it raises 600 alerts a day and 60 of them are real events, while at a stricter threshold it raises 100 alerts and 40 are real events (per day, from a retrospective replay, with the stricter alerts a subset of the current alerts). Compute sensitivity and positive predictive value at both thresholds and the precision of the extra 500 alerts, then say which threshold you would recommend and who must agree.", 'HD')
# A pacing
c0 = 15000/30 + 9000/20; c1 = 9000/30 + 15000/20
assert c0 == 950 and c1 == 1050 and c1-c0 == 100 and 15000+9000 == 24000 and 15000-6000 == 9000
add(3, '🟡', "Ads: A campaign has a daily budget of 24,000 and without pacing it spends 15,000 by 09:00 at a cost per conversion of 30, while the remaining 9,000 is spent after 09:00 at a cost per conversion of 20 (measured yesterday). Moving 6,000 of the early spend to the later period would change conversions by how many if the later cost per conversion stayed at 20, which is an optimistic upper bound? Say why that cost might not stay at 20 and how a pacing controller would use feedback.", 'AP')
# F collections
assert 3000*0.4 == 1200 and 300*0.35 == 105 and round(3000*0.05) == 150 and 150*8000 == 1200000 and 3000*150 == 450000
add(3, '🟡', "Fintech: A collections team can call 3,000 of 10,000 delinquent accounts a day, and the model ranks accounts by probability of payment. Among 3,000 called top-ranked accounts, 1,200 (40%) paid within 14 days, while among a random holdout of 300 top-ranked accounts that were not called, 105 (35%, a small holdout) paid on their own. An incremental payment is worth 8,000 and a call costs 150, so compute the incremental payments in the called group and the net value, and explain why the model should be built for the effect of calling rather than for payment probability.", 'ED:collections prioritisation and uplift modelling in credit-risk material')
# H clinician override
assert 700+300 == 1000 and 35+90 == 125 and 125/1000 == 0.125 and 90/125 == 0.72 and 700-35 == 665
add(3, '🟡', "Healthcare: In a pilot, 1,000 high-risk alerts were raised and clinicians overrode 700 of them. Of the 700 overridden alerts, 35 were followed by a deterioration event, and of the 300 acted-on alerts, 90 were followed by one (counts from a measured pilot). Compute the share of all alerts followed by an event and the share of alert-followed events that were in acted-on alerts, and explain why you should not conclude that clinicians are simply right or wrong, and what you would do about trust.", 'HD')
# A invalid traffic
assert 2000000*0.10 == 200000 and (1800000*0.02)/2000000 == 0.018
add(3, '🟡', "Ads: A publisher sends 2,000,000 clicks in a day and 200,000 of them (10% of clicks) are later classified as invalid, with the advertiser credited back for them after 3 days. The conversion rate per click is 2.0% for valid clicks and 0% for invalid clicks, so the measured blended rate is 1.8% (rates from a measured sample). Explain how training the click and conversion models on the raw clicks distorts bids, how you would handle the 3-day delay in labels, and what you would tell the publisher account team.", 'AP')

# ======================= 3 stars, red =======================
rej_bad = 70000*0.12
assert 30000*0.04 == 1200 and round(rej_bad) == 8400 and abs((1200+rej_bad)/100000-0.096) < 1e-12 and 100000-30000 == 70000
add(3, '🔴', "Fintech: A lender approved 30,000 of 100,000 applicants last year (30%) and 1,200 of the approved (4%) defaulted within 12 months, measured on matured outcomes. A new model is trained only on the approved applicants and the 70,000 rejected applicants have no outcome. If rejects defaulted at 3 times the approved rate, the population default rate would be 9.6%, which is one scenario and not a measurement. Explain the bias, the reject-inference options and their limits, and what low-risk experiment would give you real outcomes on rejects.", 'FC')
# E censored demand
unc = 400/10*14
avg_naive = (5*400+560+540)/7; avg_unc = (5*560+560+540)/7
assert unc == 560 and round(avg_naive) == 443 and abs(avg_unc-557.14) < 0.01
add(3, '🔴', "E-commerce: A product's selling window runs from 08:00 to 22:00 (14 hours) and it sold out at 18:00 on 5 of the last 7 days with 400 units sold on each of those days, while on the other 2 days it sold 560 and 540. A forecast trained on sales averages 443 units a day and next week's stock is planned from it. Assuming flat hourly demand, which is an assumption to test, estimate the uncensored daily demand on the stock-out days and the 7-day average, and explain how you would model demand from censored sales and handle a price change in the same week.", 'ED:censored demand and stock-outs in forecasting and pricing material')
# H kappa
n=1000; a=150; b=60; c=40; dd=750
po=(a+dd)/n; pa=(a+b)/n; pb=(a+c)/n; pe=pa*pb+(1-pa)*(1-pb); k=(po-pe)/(1-pe)
assert a+b+c+dd == n and po == 0.9 and abs(pe-0.6798) < 1e-9 and abs(k-0.6877) < 1e-3
add(3, '🔴', "Healthcare: Two radiologists independently labelled the same 1,000 scans: both marked 150 as abnormal, both marked 750 as normal, reader A alone marked 60 as abnormal and reader B alone marked 40. The raw agreement is 90%, but the team plans to train on reader A's labels as ground truth and to quote accuracy against them. Compute Cohen's kappa, explain what it implies for the model's ceiling and evaluation, and describe how you would build a better reference standard.", 'HD')
# A signal loss
assert abs(7000/0.6-11666.67) < 0.01 and abs(7000/0.6/10000-1.1667) < 1e-3 and abs((10000-7000)/10000-0.30) < 1e-12
add(3, '🔴', "Ads: After a platform privacy change, 60% of users allow tracking and reported attributed conversions fell from 10,000 to 7,000 a day (30% lower, relative to 10,000), while first-party total orders stayed flat at 25,000 a day. Scaling the 7,000 by 1 divided by 0.6 gives about 11,667, which is 16.7% above the earlier 10,000. Explain why the naive scale-up is probably wrong, how you would estimate true conversions and recalibrate the bidding model, and which checks you would run.", 'ED:privacy changes, consent and signal loss in ads measurement')

# ======================= 2 stars, green =======================
# F cutoff
def prof(app, br, g=1000, l=6000):
    bad = round(app*br); return (app-bad)*g - bad*l
pA, pB, pC = prof(40000, .02), prof(55000, .035), prof(70000, .06)
assert (pA, pB, pC) == (34400000, 41525000, 40600000)
assert round(55000*.035)-round(40000*.02) == 1125 and abs(1125/15000-0.075) < 1e-12
assert round(70000*.06)-round(55000*.035) == 2275 and abs(2275/15000-0.1517) < 1e-4 and abs(1000/7000-0.1429) < 1e-4
add(2, '🟢', "Fintech: A lender can set one of three cutoffs on a score. Cutoff A approves 40,000 of 100,000 applicants with a bad rate of 2% of approved, cutoff B approves 55,000 with 3.5% and cutoff C approves 70,000 with 6% (bad rates are projections). A good customer yields a profit of 1,000 and a bad one a loss of 6,000, so compute the total profit at each cutoff, the bad rate of the extra applicants between cutoffs and the break-even bad rate, then say which cutoff you would pick and what you would check first.", 'FC')
# E fake reviews
se_ = math.sqrt(0.12*0.88/500); lo, hi = 0.12-1.96*se_, 0.12+1.96*se_
assert 54/150 == 0.36 and 54/60 == 0.9 and abs(lo-0.0915) < 5e-4 and abs(hi-0.1485) < 5e-4
add(2, '🟢', "E-commerce: An audit team hand-labelled a random sample of 500 reviews and found 60 fake (12%, a sample estimate). A classifier flagged 150 of the same 500 reviews and 54 of the flagged ones were fake. Compute its precision and recall on this sample and an approximate 95% interval for the true fake share using the normal approximation, and say what you would do with the flagged reviews before taking them down.", 'EF')
# H privacy
assert 15000/120000 == 0.125
add(2, '🟢', "Healthcare: A model was trained on 120,000 patient records and 15,000 patients (12.5% of the records) later withdrew consent for research use. Retraining from scratch takes 3 days of compute plus a clinical re-validation, and the product team asks whether the deployed model can keep running. What do you tell them, what questions do you take to the privacy and compliance teams, and how would you design the pipeline so withdrawals are cheap to honour next time?", 'ED:consent withdrawal and data lineage in health-data privacy material')
# A frequency cap
vals = [round(p*20-0.05, 4) for p in (0.005, 0.003, 0.0015, 0.0005)]
assert vals == [0.05, 0.01, -0.02, -0.04]
add(2, '🟢', "Ads: For a retail campaign, the measured incremental conversion probability per user from the 1st, 2nd, 3rd and 4th impression in a week is 0.50%, 0.30%, 0.15% and 0.05%. A conversion is worth 20 and each impression costs 0.05. Compute the net value of each impression and the best weekly cap, and explain how you would check that these incremental numbers are causal.", 'AP')
# F governance
assert 120-18 == 102 and 24-18 == 6 and 102/6 == 17
add(2, '🟢', "Fintech: A bank has 120 models in its inventory and 18 of them are in the high-risk tier. The independent validation team can complete 24 full validations a year and each high-risk model needs one every year. Compute how many validations remain for the other 102 models and how many years one pass over them would take, and say how you would tier models, trigger early reviews and use lighter-weight monitoring, leaving rules to compliance.", 'ED:model risk governance in general terms (tiering, validation capacity)')
# E size
assert 20000*0.08+80000*0.13 == 12000 and round(80000*0.05) == 4000 and 4000*150 == 600000
add(2, '🟢', "E-commerce: Of 100,000 apparel orders, 12,000 (12%) are returned for size reasons, and a size widget (use was voluntary) was used on 20,000 orders: the size-return rate is 8% for widget orders and 13% for the 80,000 others (measured). The team claims that rolling the widget out would close the 5-point gap on all 80,000 other orders and save 150 per avoided return. Compute that claimed saving and explain why it is probably overstated and how you would test it.", 'ED:size recommendation and returns in fashion e-commerce material')

# ======================= 2 stars, yellow =======================
# F AML
assert 270+24+6 == 300 and 270/3000 == 0.09 and 24/3000 == 0.008 and 6/4000 == 0.0015 and (270+24)/300 == 0.98 and 3000+3000+4000 == 10000
add(2, '🟡', "Fintech: A monitoring system raises 10,000 alerts a month and analysts confirm 300 of them as suspicious (3%), with capacity to review 6,000 alerts. A model splits the alerts into three buckets: the top 3,000 alerts hold 270 confirmed cases, the middle 3,000 hold 24 and the bottom 4,000 hold 6 (retrospective counts from a month in which all 10,000 alerts were reviewed). Compute the confirmed rate in each bucket and the share of confirmed cases found by reviewing the top two buckets, and explain what you would propose for the bottom bucket given that compliance owns any decision to stop reviewing alerts.", 'ED:KYC and AML alert triage in fintech material')
# E cart
inc = 600-500; mar = inc*800*0.25; disc = 600*80
assert inc == 100 and mar == 20000 and disc == 48000 and mar-disc == -28000 and 10000*.06 == 600
add(2, '🟡', "E-commerce: In a randomised test, 10,000 cart abandoners received a reminder with a 10% discount code and 6.0% purchased, against 5.0% of 10,000 randomly held-out abandoners, and the average order value is 800 with a 25% margin before any discount. Compute the incremental orders per 10,000 abandoners, then compare the margin on them with the discount given if we assume all 600 purchasing recipients use the code. What would you change about the offer and the targeting?", 'ED:cart abandonment and discount incrementality in e-commerce material')
# H device
tpA, tpB = 800*.88, 200*.71
assert round(tpA) == 704 and round(tpB) == 142 and round((tpA+tpB)/1000, 3) == 0.846 and 800-704 == 96 and 200-142 == 58
add(2, '🟡', "Healthcare: A chest X-ray model is tested on 10,000 images, 8,000 from scanner A and 2,000 from scanner B, with 10% of images abnormal in both groups. At the deployed threshold its sensitivity is 88% on scanner A and 71% on scanner B (measured). Compute the overall sensitivity and the abnormal scans missed in each group, and say how you would investigate the gap and what you would do before the hospital adds a third scanner model.", 'HD')
# A cold start
post = (0.015*200+2)/(200+500)
assert abs(post-0.007143) < 1e-5 and 2/500 == 0.004
add(2, '🟡', "Ads: A new campaign has 500 impressions and 2 clicks, a raw click rate of 0.4%. The platform has no history for the advertiser and the category's average click rate is 1.5%, which you treat as a prior worth 200 impressions. Compute the prior-shrunk estimate, explain why the raw number should not drive the bid, and describe an exploration plan with a stopping rule and a cap on spend.", 'AC')
# F step-up
stopped = 1200 + 0.8*600; through = 200 + 0.2*600; gen_step = 18000-600
assert 2000+18000+980000 == 1000000 and 1200+600+200 == 2000 and round(stopped) == 1680 and round(through) == 320
assert round(0.10*gen_step) == 1740 and 2000-1200 == 800
add(2, '🟡', "Fintech: In one day of 1,000,000 transactions a model sends 2,000 to a block band, 18,000 to a step-up band (an extra confirmation) and lets 980,000 pass, with measured fraud counts of 1,200 in the block band, 600 in the step-up band and 200 in the pass band. Assume blocking stops every fraud in its band, the step-up stops 80% of fraud in its band and 10% of the 17,400 genuine customers in the step-up band abandon. The fraud counts in the block band come from review and customer reports. Compute the fraud stopped, the fraud that still gets through, the genuine customers blocked and the genuine customers lost at step-up, and discuss how you would set the band edges.", 'FP')
# E catalogue
w1 = 280000*0.03; w2 = 120000*0.22
assert 400000/2000000 == 0.2 and 280000+120000 == 400000 and round(w1) == 8400 and round(w2) == 26400 and round(w1+w2) == 34800
add(2, '🟡', "E-commerce: 400,000 of 2,000,000 listings (20%) lack a colour attribute. A model can fill it, with a measured accuracy of 97% on a 1,000-item audit for the 280,000 listings where its confidence is at least 0.9 and 78% on a 1,000-item audit for the other 120,000. Compute the expected wrong colours when filling only the confident ones and when filling all, treating the audit accuracies as projections, and say how you would decide, given that wrong colours drive returns.", 'ED:catalogue attribute quality and extraction in e-commerce material')
# H multi-site
assert 100/0.04 == 2500 and 100/0.025 == 4000
add(2, '🟡', "Healthcare: A sepsis model was built at hospital 1 with an AUC of 0.88 and external tests give an AUC of 0.79 at hospital 2 and 0.84 at hospital 3, with a calibration slope of 0.6 at hospital 2 (1.0 is ideal). The sepsis rate is 4% at hospital 3 and 2.5% at hospital 2, and your team wants at least 100 expected events at each site before trusting its numbers. Compute the minimum patients needed per site and describe a rollout plan with local recalibration, monitoring and stop rules.", 'HE')
# A lookalike
assert 500000*0.008 == 4000 and 500000*0.007 == 3500 and 40000/4000 == 10 and 40000/500 == 80
add(2, '🟡', "Ads: A lookalike audience built from 10,000 past converters was shown ads, reaching 500,000 users of whom 0.80% converted (4,000), while a group of 500,000 similar users, held out at random from the same lookalike audience before serving, saw none and 0.70% of them converted (3,500). The platform report attributes all 4,000 conversions to the campaign, which spent 40,000. Compute the reported and the incremental cost per conversion, and explain what the gap means and how you would improve the audience and the test.", 'AI')
# F explain
add(2, '🟡', "Fintech: A credit model declined an applicant and the lender must give up to 4 plain-language reasons. Income and employment tenure have a correlation of 0.85, so their attribution scores flip between two retrains, and for 30 of 100 reviewed declines (30% of the sample) the top reason differs between retrains. How would you produce stable reasons, validate them, and decide what to ask compliance about the wording?", 'FC')
# E trust
assert 100*0.4 == 40 and 1000*0.4 == 400 and 1000/200 == 5 and 200*0.4 == 80
add(2, '🟡', "E-commerce: A seller-risk model flags 1,000 sellers for review, an audit of 100 randomly chosen flagged sellers confirmed 40 as fraudulent (40%, a sample), and investigators can review 200 sellers a week. Estimate the fraudulent sellers among the 1,000 flagged as a projection, the weeks to clear the queue, and the number expected in the first week if the queue is reviewed in random order. How would you order the queue instead?", 'EF')
# H LLM summaries
assert 14/200 == 0.07 and 6/200 == 0.03
add(2, '🟡', "Healthcare: An LLM drafts discharge summaries and two clinicians audited 200 of them, finding 14 with an omitted medication (7%) and 6 with an invented detail (3%), measured on that sample. Clinicians must sign every summary and say drafting saves 4 of the usual 10 minutes. Explain how you would define and measure harm, what audited error rate you would want to see before wider rollout, and what you would ask the clinical safety and compliance teams.", 'ED:LLM clinical documentation audit in 2025-2026 health-AI material')

# ======================= 2 stars, red =======================
pd_pred = 20000*0.03*10000*0.5; pd_obs = 900*10000*0.5
assert 900/20000 == 0.045 and round(pd_pred) == 3000000 and round(pd_obs) == 4500000 and round(pd_obs-pd_pred) == 1500000
add(2, '🔴', "Fintech: A credit model's average predicted 12-month default probability is 3.0% across a portfolio of 20,000 loans, but 900 of them defaulted (4.5%, matured outcomes) while the AUC is unchanged at 0.80. Exposure is 10,000 per loan and the loss given default is assumed to be 50%. Compute the expected loss predicted, the loss from observed defaults at the assumed loss given default, and the shortfall, and explain the possible causes, whether you would recalibrate or rebuild, and how this goes through model governance.", 'FC')
# E pricing cannibalisation
assert 1000*100 == 100000 and 120000*450 - 100000*500 == 4000000 and 4000*60 == 240000 and 228000-240000 == -12000 and -12000*500 == -6000000 and 4000000-6000000 == -2000000
add(2, '🔴', "E-commerce: A price test cut the price by 10% on 1,000 items from 500 to 450 and daily units on those items rose 20% relative, from 100,000 to 120,000, while 4,000 close substitute items fell 5% relative, from 240,000 to 228,000 units a day at an unchanged price of 500 (projections from a pilot). Compute the item-level and the whole-category change in revenue per day, and explain how you would design the test to capture cannibalisation.", 'ED:price tests with substitution and interference in marketplace material')
# H treatment contamination
assert 1000/20000 == 0.05 and 800/20000 == 0.04
add(2, '🔴', "Healthcare: A deterioration alert model was trained on labels of ICU transfer within 24 hours. After launch, transfers fell from 1,000 to 800 per 20,000 admissions (5.0% to 4.0%, absolute) and the measured positive predictive value of alerts is 18% in live use against 30% in a retrospective replay at the same alert volume of about 1,000 alerts per 20,000 admissions. Explain how effective alerts can look like false positives, why monitoring against the original label can mislead, and how you would evaluate and retrain safely.", 'HD')
# A delayed feedback
obs = [.5, .7, .8, .9, .95, .98, 1.0]; mo = sum(obs)/7
assert abs(mo-0.8329) < 1e-3 and abs(1-mo-0.1671) < 1e-3
add(2, '🔴', "Ads: Conversions arrive late, and the share of eventual conversions already observed is 50% for clicks 0 days old, 70% at 1 day, 80% at 2, 90% at 3, 95% at 4, 98% at 5 and 100% at 6 days. A conversion model is retrained daily on the last 7 days of clicks (ages 0 to 6 days, equal click volume per age), labelling unconverted clicks as negative. Compute the average share of conversions observed across those 7 ages and the relative underestimate of the conversion rate, and describe a delayed-feedback fix.", 'AC')
# A first price
sur = {b: round((10-b)*p, 4) for b, p in {4: .2, 6: .45, 7: .6, 8: .75, 9: .88, 10: .95}.items()}
assert sur == {4: 1.2, 6: 1.8, 7: 1.8, 8: 1.5, 9: 0.88, 10: 0.0}
add(2, '🔴', "Ads: After an exchange moves from second-price to first-price auctions, an impression is worth 10 to you. From logged auctions your estimated win probability is 20% at a bid of 4, 45% at 6, 60% at 7, 75% at 8, 88% at 9 and 95% at 10 (estimates). Under first price you pay your bid when you win, so compute the expected surplus (value minus bid, times win probability) at each bid, name the best bid and explain how you would break the tie, estimate the win curve and spot when it breaks.", 'AP')
# A geo lift
assert 100000000*0.04 == 4000000 and 4000000/1000000 == 4
add(2, '🔴', "Ads: Total sales are 100,000,000 over a test period spread evenly across 50 regions, and last-click attribution credits online video with 1,000,000 of them (1% of sales). A geo test paused video in 10 randomly chosen regions and sales there were 4% lower than the kept regions' with-video level of 2,000,000 per region. Project the whole-country sales attributable to video if the effect is uniform, compare it with the last-click credit, and explain the assumptions and what a 10-region test can and cannot tell you.", 'AI')

# ======================= 1 star, green =======================
assert 1000000*0.06 == 60000 and 60000*0.4 == 24000 and 60000*0.2 == 12000
add(1, '🟢', "E-commerce: 6% of 1,000,000 daily searches return no results, which is 60,000 searches, and a manual review of 500 of those found 200 (40%) were spelling or synonym problems and 100 (20%) were products the catalogue genuinely lacks. Estimate the daily searches in each of those two groups as projections, and explain what you would build first, how you would measure its effect, and how you would pass the missing-product signal to sellers.", 'EP')
assert 600/50000 == 0.012
add(1, '🟢', "Healthcare: A research extract of 50,000 patient records is prepared for a partner, with age in years, a 3-digit postcode area and sex as the only quasi-identifiers. Counting shows 4,000 distinct combinations of these three fields and 600 combinations appear exactly once. Compute the share of records that are unique on these fields and explain why it matters, what generalisation or suppression you would try, and which questions go to the privacy officer before anything is shared.", 'ED:de-identification and re-identification risk in health-data sharing material')

# ======================= 1 star, yellow =======================
assert 15000*60 == 900000 and 20/200 == 0.1 and 180/15000 == 0.012 and abs(20/35000-0.00057) < 1e-5 and 35000+15000 == 50000 and 35000/50000 == 0.7 and 50000*0.004 == 200
add(1, '🟡', "Fintech: Of 50,000 monthly onboarding applications, 0.4% (200) are synthetic or stolen identities, a retrospective estimate. A document-and-face score auto-approves 35,000 applications (70%) and sends 15,000 to manual review at 60 each, and the auto-approve band contains 20 of the 200 bad identities. Compute the manual review cost, the share of bad identities that skip review, and the bad-identity rate in each band, and describe how you would revisit the band edge while leaving the risk appetite to the business and compliance.", 'ED:KYC identity verification triage in fintech onboarding material')
assert abs(0.24/4.00-0.06) < 1e-12 and abs(2.5/500-0.005) < 1e-12 and 500.0-497.5 == 2.5
add(1, '🟡', "E-commerce: A new recommender raised homepage click-through from 4.00% to 4.24% (a 6% relative rise, 0.24 points absolute, measured in an A/B test), while GMV per user fell from 500.0 to 497.5 (0.5% relative) and the share of impressions on long-tail items fell from 30% to 18% (absolute points). Explain the possible mechanism, which further metrics you would inspect, and how you would decide whether to ship.", 'ED:recommendation diversity and long-tail exposure in e-commerce material')
add(1, '🟡', "Healthcare: A deterioration model uses a feature 'lactate was measured' because clinicians order the test when they are worried. At hospital A the test is ordered for 60% of patients and the model's AUC is 0.85, while at hospital B it is ordered for 20% and the AUC is 0.74 (both measured, on different patient populations). Explain why the feature transports poorly, how to treat informative missingness across sites, and what you would validate before the model runs at hospital B.", 'HE')
sec = math.sqrt(0.025*0.975/2000)
assert abs(sec-0.003491) < 1e-5 and 40/2000 == 0.02 and 50/2000 == 0.025 and 46/2000 == 0.023
add(1, '🟡', "Ads: Three creatives were each shown 2,000 times and got 40, 50 and 46 clicks, which are rates of 2.0%, 2.5% and 2.3%. The standard error of creative B's own rate is about 0.35 points (the square root of 0.025 times 0.975 over 2,000), while the standard error of the difference between B and A is about 0.47 points. How would you decide how to split the next day's impressions, why might you not simply pick B, and how would you handle creative fatigue?", 'ED:creative selection with bandits in ads system-design material')
add(1, '🟡', "Fintech: For thin-file applicants, adding a phone-usage feature set lifts AUC from 0.66 to 0.71 (0.05 absolute, measured among the 70% of applicants who have the features, on a back-test of matured loans that covers approved applicants only) and the features exist for 70% of applicants. Explain what you would check for stability, gaming, proxy risk for protected traits and consent, what the lender should ask compliance, and how you would roll the features out.", 'FC')

# ======================= 1 star, red =======================
assert 500*0.7 == 350 and 350/1000 == 0.35
add(1, '🔴', "Fintech: A fraud model's flagged transactions have a chargeback 50% of the time (500 of 1,000 flagged, measured), but an audit finds 30% of chargebacks are friendly fraud, where the genuine cardholder disputes a purchase they made. Compute the minimum share of flagged transactions that are true fraud (treating the 500 flags without a chargeback as not fraud) if the 30% applies to the 500 flagged chargebacks, and explain how label noise from chargebacks affects training, evaluation and customer treatment.", 'ED:chargeback labels and friendly fraud in payments material')
assert 20000/2000000 == 0.01 and 48000/400000 == 0.12 and 20000*0.75 == 15000
add(1, '🔴', "E-commerce: 20,000 of 2,000,000 customers (1%) are flagged as serial returners and account for 48,000 of 400,000 returns (12% of returns), while a review of 200 flagged customers found 150 (75%, a sample) were abusing the policy and 50 were legitimate heavy buyers. Estimate the abusers among the 20,000 as a projection, and discuss how to act, how to evaluate it without being unfair to the other 25%, and what you would ask the policy and legal teams.", 'ED:return abuse and marketplace trust in e-commerce material')
assert abs(math.sqrt(0.8*0.2/400)-0.02) < 1e-12
add(1, '🔴', "Healthcare: A deployed model's sensitivity was 0.82 on its locked test set. A retrained version shows 0.80 on the same set with 400 positives, a standard error of about 0.02 for the new sensitivity alone (the square root of 0.8 times 0.2 over 400), and the team wants to ship it because its calibration is better. The comparison is paired on the same patients: the old model caught 20 positives that the new one missed, and the new one caught 12 that the old one missed. How do you decide whether this is acceptable, what margin and evidence would you pre-specify, and what would you ask the regulatory team about classifying the change?", 'ED:model updates and change control in clinical AI, regulatory humility')
assert 5/8 == 0.625 and abs(5*math.sqrt(7)-13.229) < 1e-3 and abs(5*math.sqrt(7)/56-0.2362) < 1e-3
add(1, '🔴', "Ads: A privacy-preserving report gives per-campaign daily conversion counts with random noise of standard deviation 5 added to each count, independently each day. A small campaign has about 8 true conversions a day. Compute the noise as a share of the daily count and as a share of a 7-day total of 56 (the noise standard deviation grows with the square root of 7), and explain how you would still optimise bids and judge that campaign.", 'ED:noisy aggregated conversion reporting in privacy-preserving ads measurement')

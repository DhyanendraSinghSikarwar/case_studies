# Growth, CRM and Experimentation Cases - Research Notes (agent 4)

Compiled 2026-10-17. Only pages actually fetched are listed under Source Links. Many Medium, DoorDash, BSE and Swiggy Bytes pages returned HTTP 403 or connection errors, so several primary documents could not be read; where a claim came only from a search-result summary it is marked "(search snippet, unverified)" and is not used as a documented fact.

## Case R1 — Switchback vs A/B experimentation in two-sided marketplaces (Cabify documented; Flipkart's early A/B framework as the Indian reference)
**Company:** Cabify (substitute; Spain/LatAm ride-hailing marketplace). Indian reference: Flipkart (2012 A/B framework). Swiggy's in-house Experimentation Platform (XP) exists per search-result snippets, but its posts could not be fetched.
**Industry:** Ride-hailing marketplace (substitute); Indian ecommerce (reference)
**Business Area:** Product experimentation / growth analytics
**Problem Type:** Experiment design under interference (A/B vs switchback), experimentation platform
**Evidence Level:** Medium (A for Cabify, a named engineer's post; the Indian leg is only a 2012 press account with no statistics; no Indian method-level source was readable)
**Primary Sources:** Cabify engineering blog (Albert Rego, 4 Mar 2026); CIO India (Varsha Chidambaram, 21 May 2012) on Flipkart's framework.

### 1. Business Problem
Documented (Cabify): A/B tests split users into fixed groups, but some metrics are marketplace-wide. If treatment users create more journeys, they consume the shared driver pool and lower the success rate for control users. The post calls this cross-group interference "cannibalization", which makes A/B results misleading for such metrics.
Documented (Flipkart, 2012): Flipkart wanted to ship site changes without lengthy process. Amod Malviya (VP Engineering) designed a framework with a real-time metrics dashboard plus an A/B component.
Note: Swiggy/Zomato face the same shared-supply (delivery partner) structure, but the source for that is my inference, not a fetched page.

### 2. Business Question
Can a change to a marketplace-level algorithm or message be evaluated when treatment and control share supply? (Cabify example: standard ETA message vs a "more than 6 minutes" message.) For Flipkart: does a new homepage design hurt sales if shown to a slice of traffic?

### 3. Data Available
| Data | Description |
|---|---|
| Interval-level marketplace metrics (Cabify) | Performance (e.g. journey success) measured in each time interval, each interval is one sample |
| Journey / request logs (Cabify) | Journeys can start in one interval and finish in another (carryover) |
| Real-time site metrics (Flipkart, 2012) | Transaction rate etc. on a dashboard with threshold alerts |
| Dataset sizes, dates, schema | Not publicly disclosed (ND) |

### 4. Data Science Approach
Cabify: switchback design. All users see the same version at a given time; the group is determined by the time slot, so a user may experience both versions. Interval length is chosen to include all hour/day combinations (peak and off-peak), spread samples across hours and days, and fit the planned experiment duration. Example uses 53-minute intervals (a prime number, chosen to avoid cycling effects); alternatives mentioned: 58, 112, 29 minutes. Carryover is handled by switching less often when effects are persistent and by washout periods that drop early-treatment data. Duration depends on MDE and sample size, plus cost of running, uncertainty in sample rate, and blocking with other experiments (e.g. by region).
Flipkart 2012: 10% of traffic routed to the new version; metrics tool measures impact; if sales dip the change is rolled back.

### 5. Statistical Analysis
Cabify: performance compared across alternating intervals; sample-size/MDE logic "the same statistics as A/B tests"; washout. Specific test statistic, variance estimator, or CUPED-type adjustment: ND in the fetched post. Flipkart 2012: no statistics described (ND).
(DoorDash material on cluster-robust standard errors and CUPAC ">25% shorter switchback tests" appeared only in a search snippet; the DoorDash pages returned 403, so it is not treated as documented.)

### 6. Machine Learning
- Model(s): None (design/statistics case); ND
- Target variable: Marketplace-level success metric per interval (Cabify); ND beyond that
- Features: ND
- Validation approach: ND
- Metrics: ND

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Flipkart in-house A/B framework + metrics dashboard (2012) | Traffic split, real-time metrics on screens |
| Cabify internal switchback tooling | ND (tooling not named) |

### 8. Business Decision
Cabify: use switchback rather than user-level A/B for marketplace-wide metrics. Flipkart: roll out or roll back UI changes based on live metrics, accepting some risk to keep a "fearless culture of innovation" (Malviya).

### 9. Business Impact
No numeric lift stated for Cabify's example (ND). Flipkart 2012 article: tool introduced mid-2010; article context figures (company-reported/press): sales of Rs 75 crore a month, revenue doubling every quarter for eight quarters. These are not attributed causally to the framework.

### 10. What a Data Scientist Can Learn *(interpretation)*
Be able to say when user-level randomisation breaks (shared supply), what the unit of analysis becomes (the interval), why a prime interval length helps, and how washout trades bias for sample size. An interviewer will also expect power calculation, SRM checks and guardrail metrics, none of which these sources document.

### 11. Source Links
- Cabify Engineering, "Why do you need switchback experimentation", Albert Rego, 4 Mar 2026 - https://tech.cabify.com/blog/engineering/why-do-you-need-switchback-experimentation
- CIO India, "Flipkart Drives Innovation Through Intelligent use of IT", 21 May 2012 - https://www.cio.com/article/215584/flipkart-drives-innovation-through-intelligent-use-of-it.html

## Case R2 — Predicted lifetime value (pLTV) of new customers for bid optimisation at Swiggy
**Company:** Swiggy (Food delivery and Instamart)
**Industry:** Food delivery / quick commerce
**Business Area:** Customer acquisition and lifetime value
**Problem Type:** Customer lifetime value prediction (cold start), multi-task learning
**Evidence Level:** Medium (B: InfoQ report of Swiggy's own Bytes post, quoting named Swiggy staff; the original Medium post returned 403 so details come second-hand). Classic RFM-based segmentation at Nykaa/Myntra/FirstCry/Flipkart: no company source found.
**Primary Sources:** InfoQ, "Swiggy Uses 350+ Features and Multi-Task MLP to Predict Customer Lifetime Value", Leela Kumili, 2 Sep 2026; original Swiggy Bytes post (not read).

### 1. Business Problem
Documented (via InfoQ): Predict the long-term value of new customers across Food and Instamart before their first order, so advertising bids optimise for long-term value instead of short-term conversion. Sparse early signals and a skewed target: many new users place no orders in 30 days while a small group generates much higher lifetime value.

### 2. Business Question
Can pre-first-order information rank new users by future value well enough to differentiate ad bids?

### 3. Data Available
| Data | Description |
|---|---|
| Pre-first-order features (350+) | Acquisition channel, device and fraud signals, geographic behaviour, complaint history, Instamart category affinity, order behaviour, payment patterns, socioeconomic indicators |
| Dataset size / time range | Not publicly disclosed (ND) |

### 4. Data Science Approach
Features built only from information available before first order (cold-start). A relatively simple MLP with three shared hidden layers and task-specific heads for Food and Instamart. Output used with Google tROAS bidding. Next step stated: probabilistic pLTV to represent uncertainty.

### 5. Statistical Analysis
MAE and MAPE judged insufficient because of many zeros and a long tail. Evaluation by ranking: predicted and actual values split into ten quantiles; Spearman correlation and decile "diagonal coverage". Hypothesis tests on the A/B: ND.

### 6. Machine Learning
- Model(s): Multi-task MLP, 3 shared hidden layers, heads for Food and Instamart; parameters reduced from 363,000 to 135,000 ("63% reduction"); the four-head version performed marginally better. Layer sizes/activations: ND
- Target variable: Lifetime value (primary); order count (auxiliary task)
- Features: 350+ pre-first-order features (categories above)
- Validation approach: Decile-ranking comparison of predicted vs actual; split scheme ND
- Metrics: Spearman above 0.75 for both Food and Instamart; diagonal coverage across deciles 70% to 80%

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Google Ads tROAS bidding | Consumes pLTV signal |
| ML framework | Not named (ND) |

### 8. Business Decision
Use the in-house pLTV signal for acquisition bidding instead of a third-party pLTV platform.

### 9. Business Impact
In production A/B, versus a third-party pLTV platform, the in-house model gave "higher retention and gross order value per acquired user, with no additional platform costs"; the external platform acquired more users per dollar. Exact figures: ND (InfoQ states none).

### 10. What a Data Scientist Can Learn *(interpretation)*
Zero-inflated, heavy-tailed LTV targets are better evaluated by ranking than by MAE; a model is judged by the downstream decision (bid), and a comparison against a vendor shows the CAC-versus-quality trade-off. Standard interview material: RFM, BG/NBD + Gamma-Gamma, hurdle models, calibration.

### 11. Source Links
- InfoQ, "Swiggy Uses 350+ Features and Multi-Task MLP to Predict Customer Lifetime Value", 2 Sep 2026 - https://www.infoq.com/news/2026/09/swiggy-pltv-multitask-mlp/

## Case R3 — Zomato Gold relaunch (2023) and Flipkart Plus tiering as membership design
**Company:** Zomato (primary); Flipkart (design contrast)
**Industry:** Food delivery; ecommerce
**Business Area:** Loyalty / subscription and retention
**Problem Type:** Membership programme design, retention, frequency uplift
**Evidence Level:** Weak-to-Medium (A for programme design and CEO statements via press coverage of the shareholder letter; no model or experiment method is public; the shareholder-letter PDFs themselves returned 403)
**Primary Sources:** Business Today (9 Feb 2023, 22 Mar 2023) reporting Zomato's Q3 FY23 letter; Flipkart Stories (15 Aug 2023).

### 1. Business Problem
Documented: Zomato relaunched Gold in January 2023 with a redesign that CEO Deepinder Goyal said was built on lessons from past years and is "more sustainable for customers, restaurant partners, and Zomato's P&L". It was expected to "drive loyalty and higher frequency of ordering going forward".

### 2. Business Question
Can a redesigned paid membership raise order frequency and loyalty without destroying unit economics? (Stated framing, not a documented analytical question.)

### 3. Data Available
| Data | Description |
|---|---|
| Order history | Not publicly disclosed (ND) as an input to design |
| Flipkart Plus eligibility data | Successful transactions in last 365 days (rule-based) |

### 4. Data Science Approach
Only programme design is public. Zomato Gold: Rs 149 for three months introductory price; unlimited free delivery within 10 km or on orders above Rs 199; "On Time Guarantee" Rs 100 coupons for delayed orders; up to 30% off delivery and up to 40% flat off dining at 25,000+ restaurants. Flipkart Plus: earned tiers, Silver at 15 and Gold at 25 successful transactions in 365 days, auto-activation, SuperCoins 1 or 2 per Rs 100, caps of 50 per month and 15 per order. Any modelling behind these thresholds: ND.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- Model(s): ND
- Target variable: ND
- Features: ND
- Validation approach: ND
- Metrics: ND

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Not disclosed | ND |

### 8. Business Decision
Zomato: relaunch Gold at a low entry price with delivery, on-time-guarantee and dining benefits. Flipkart: auto-enrol based on trailing-12-month transaction counts rather than a coin threshold (earlier 200-SuperCoin criterion per a search snippet, unverified).

### 9. Business Impact
Company-reported: "over nine lakh" Gold members within a month of relaunch (Business Today, 9 Feb 2023). HSBC (external broker, not company) says Gold helped Zomato take share from Swiggy in Q4FY23. Shareholder-letter figures that appeared only in a search snippet and are unverified here: Gold about 30% of food-delivery GOV (Mar-23) with order frequency up about 60% post joining; about 40% of food GOV in Q2 FY24; Gold orders worse on contribution margin. Swiggy One figures (7.40 vs 4.50 orders per member, 5.71 million members in Q1 FY25) also came only from a snippet of a third-party newsletter and are unverified. Flipkart: no membership size or share of transactions published on the fetched page.

### 10. What a Data Scientist Can Learn *(interpretation)*
Members self-select, so "frequency up 60% after joining" is not a causal effect; interviewers expect propensity matching, difference-in-differences or holdout design, and contribution-margin (not GOV) as the success metric. Threshold-based tiers are a design lever to analyse with elasticity or breakpoint analysis.

### 11. Source Links
- Business Today, "Zomato Gold adds 9 lakh members in a month...", Binu Paul, 9 Feb 2023 - https://www.businesstoday.in/amp/latest/corporate/story/zomato-gold-adds-9-lakh-members-in-a-month-10-minute-delivery-service-to-be-replaced-with-home-style-meal-service-369712-2023-02-09
- Business Today, "Zomato Gold or Swiggy One: Who's winning the loyalty programme race?", Sohini Mitter, 22 Mar 2023 - https://www.businesstoday.in/amp/entrepreneurship/story/zomato-gold-or-swiggy-one-whos-winning-the-loyalty-programme-race-374408-2023-03-22
- Flipkart Stories, Flipkart Plus programme page, 15 Aug 2023 - https://stories.flipkart.com/flipkart-plus-premium-loyalty-memberships
- Inc42, Swiggy FY26 metrics (platform frequency 4.07, MTUs 23.5 Mn; no Swiggy One data), 24 Jul 2026 - https://inc42.com/buzz/over-35-of-swiggy-users-try-multiple-services-but-order-frequency-slips/

## Case R4 — Real-time personalised coupon allocation under a budget (Meituan Bike; substitute for Indian companies)
**Company:** Meituan (substitute; no Indian company source with method detail found)
**Industry:** Bike-sharing subscription / local-services platform (China)
**Business Area:** Promotions and discount targeting
**Problem Type:** Personalised discount allocation under budget constraint (predict-then-optimise)
**Evidence Level:** Strong (C: paper by company team with online A/B test; but not Indian)
**Primary Sources:** Dai, Li, Zhu, Lin, Huang, "Data-Driven Real-time Coupon Allocation in the Online Platform", arXiv:2406.05987v3 (17 Jun 2024). Dai, Lin and Huang are at Meituan.

### 1. Business Problem
Meituan Bike sells monthly subscriptions and wants a personalised coupon for each arriving customer. The old offline integer-program system set coupons a day ahead, could not use same-day information, had to group customers and stored a value per user. The new system must decide within 50 ms and stay within a marketing budget under uncertain traffic.

### 2. Business Question
Which coupon level should each arriving user get to maximise revenue (price x conversion) subject to an average-price budget?

### 3. Data Available
| Data | Description |
|---|---|
| Random-traffic group | About 3 million user-level entries (20% of traffic across roughly 100 Chinese cities), split 80/20 train/test |
| Features | Over 200 customer, riding-behaviour and transaction features |
| Online test population | 3,867,738 random users in two cities, February 2024, about a month |

### 4. Data Science Approach
Predict conversion rate (CVR) for each coupon level; calibrate so CVR is non-increasing in price; relax the integer program via a Lagrangian dual; choose the coupon by argmax over the coupon ladder for a given multiplier lambda; initialise lambda offline by trisection search; a PID controller adjusts lambda during the day to keep average offered price near budget.

### 5. Statistical Analysis
Isotonic regression for calibration; PCOC (predicted-to-observed conversion) check; online randomised comparison across groups (Random, Manual, Offline-IP, LDM, LDM-IR). Significance testing: ND in the summary I read (the last 26k characters of the page were not read).

### 6. Machine Learning
- Model(s): XGBoost CVR model with isotonic-regression calibration
- Target variable: Conversion (CVR) at each coupon level
- Features: 200+ customer, riding-behaviour, transaction features
- Validation approach: 80/20 split on random-traffic data; offline runtime comparison; PID simulation; online A/B
- Metrics: AUC 0.891 (plain and calibrated); PCOC 0.971 to 0.982 after calibration; CVR, average price, price x CVR

### 7. Tools & Technology
| Tool | Use |
|---|---|
| XGBoost | CVR model |
| Lagrangian dual + trisection + PID controller | Allocation and budget control, 50 ms decisions |

### 8. Business Decision
Replace the offline integer-program allocation with the real-time LDM-IR system, rolled out beyond the test.

### 9. Business Impact
Company/author-reported. City B online test: LDM-IR price x CVR 2.15 vs Offline-IP 2.09; authors report "a 2.8% revenue gain per exposed user for LDM-IR over Offline-IP, about CNY 6 million per month per 100 million exposed users". City A: LDM-IR CVR 14.49% vs Random 12.93%. Abstract: 0.7% revenue uptick, about CNY 8 million annual profit; deployed to over 100 million users in 110+ cities as of May 2024. Group-level solve 0.28 s vs 83.42 s for the offline IP in City C. PID kept average price within about 1% of target versus about 3% overshoot without control.

### 10. What a Data Scientist Can Learn *(interpretation)*
Predict-then-optimise with a budget constraint is the standard template; calibration matters because the optimiser consumes probabilities, not ranks. Indian practice likely uses uplift models rather than pure CVR, but I found no public Indian method source (Meesho, Flipkart, Swiggy, Zomato searches returned nothing usable).

### 11. Source Links
- arXiv:2406.05987v3, "Data-Driven Real-time Coupon Allocation in the Online Platform", 17 Jun 2024 - https://arxiv.org/html/2406.05987v3

## Case R5 — Meesho notification volume, relevance and send-time experiments
**Company:** Meesho
**Industry:** Social / value ecommerce marketplace
**Business Area:** CRM / push notifications
**Problem Type:** Notification frequency, content relevance and send-time personalisation
**Evidence Level:** Weak (A: named executive on a panel, but only outcomes and framing; no method, data or numbers beyond volume)
**Primary Sources:** CleverTap blog, "How Meesho Created an App Experience to Serve an Untapped Market (Part 2 of 2)", 14 Feb 2023; panel with Kirti Varun Avasarala (Meesho CPO) and Abhishek Gupta (CleverTap CCO).

### 1. Business Problem
Conventional wisdom, as Avasarala put it: "Send too many notifications, and customers will uninstall your app because you're annoying them." Meesho tested this assumption.

### 2. Business Question
Does a much higher notification volume hurt uninstalls and retention, and what content, volume and timing should each customer receive?

### 3. Data Available
| Data | Description |
|---|---|
| Analysis, customer conversations, usage patterns | Mentioned qualitatively; specifics ND |

### 4. Data Science Approach
Only the framing is public. Meesho experimented with which content to send to each customer, and both notification volume and time of day of sending were personalised. Model, design, holdouts: ND.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- Model(s): ND (a separate talk summary says Meesho's Chief Data Scientist mentions ML for personalised push, from a search snippet only)
- Target variable: ND
- Features: ND
- Validation approach: ND
- Metrics: Engagement, uninstalls, retention named qualitatively

### 7. Tools & Technology
| Tool | Use |
|---|---|
| CleverTap | Engagement platform (the panel was hosted by CleverTap; Meesho named as a customer by Gupta) |

### 8. Business Decision
Send roughly 20 to 30 notifications per day, personalising content, volume and timing.

### 9. Business Impact
Company executive statement: engagement increased, uninstalls unaffected, retention "stayed strong"; Avasarala called it "very, very counterintuitive" and reported "very, very high engagement". No percentages (ND).

### 10. What a Data Scientist Can Learn *(interpretation)*
Frequency is context-dependent (Meesho is "a sort of hybrid of a social app and an ecommerce app"); test with long-run holdouts that track uninstall and opt-out, not only click-through. Expect questions on bandits for send-time, uplift per user and fatigue modelling.

### 11. Source Links
- CleverTap blog, "How Meesho Created an App Experience to Serve an Untapped Market (Part 2 of 2)", 14 Feb 2023 - https://clevertap.com/?p=56922

## Case R6 — Marketing mix modelling plus geo-lift experiments at Honasa Consumer
**Company:** Honasa Consumer (Mamaearth parent). Nykaa, FirstCry, Flipkart and Swiggy: no usable source found.
**Industry:** D2C personal care (omnichannel, including ecommerce)
**Business Area:** Marketing measurement
**Problem Type:** MMM, incrementality (geo lift)
**Evidence Level:** Weak (A: named SVP quoted by Google; vendor-hosted write-up with no numbers or method detail)
**Primary Sources:** Think with Google India, MMM mindset shifts, Isha Puri and Naveen Yadav, December 2024; quotes from Vipul Maheshwari, SVP Product and Analytics, Honasa.

### 1. Business Problem
Honasa broadened its MMM to cover a wide range of factors rather than a narrow set, to make better-considered marketing decisions to reach millennial customers across India (as summarised from the page).

### 2. Business Question
Which marketing inputs drive sales, and how do strategies perform locally by geography?

### 3. Data Available
| Data | Description |
|---|---|
| Sales and marketing data, external factors | Maheshwari: "We analysed everything from sales and marketing data to external factors." Granularity, history, channels: ND |
| Geo lift experiment data | Maheshwari: "We also layered in our geo lift experiments" |

### 4. Data Science Approach
MMM combined with geo-lift experiments to see how strategies affect performance regionally. Model form, priors, calibration procedure: ND. The same page notes that in India MMM is often seen as "once-and-done" and argues for re-running (from a search summary of the Google page; not independently quoted).

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- Model(s): ND
- Target variable: ND (sales implied)
- Features: ND
- Validation approach: ND
- Metrics: ND

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Not named | ND |

### 8. Business Decision
Use MMM outputs to guide marketing decisions for millennial audiences; specifics ND.

### 9. Business Impact
ND. The page gives no Honasa-specific results.

### 10. What a Data Scientist Can Learn *(interpretation)*
Interviewers expect: MMM as regression with adstock and saturation (Bayesian, e.g. Robyn/Meridian-style), calibrated by geo-lift or holdout tests, and why last-click attribution over-credits bottom-funnel channels. This page confirms only that Indian firms pair the two.

### 11. Source Links
- Think with Google India, "Marketing mix modelling mindset shifts", Dec 2024 - https://business.google.com/in/think/measurement/marketing-mix-modelling-mindset-shifts/

## Notes for the notebook author

### R1 Experimentation / switchback
(a) Calibrate to: Cabify example interval 53 min (alternatives 58, 112, 29); Flipkart 2012 routed 10% of traffic to a new design; sample unit equals the interval, so n is the number of intervals not trips; washout drops early-window data (Cabify). No lift figures are public.
(b) Expected techniques: power/MDE and sample size, SRM check, CUPED variance reduction, guardrail metrics, multiple testing correction, sequential testing, switchback with cluster-robust errors, carryover/washout.
(c) Very common.

### R2 LTV / segmentation
(a) Swiggy: 350+ pre-first-order features; MLP with 3 shared hidden layers; parameters 363,000 to 135,000; Spearman above 0.75; diagonal coverage 70% to 80%; many users have zero orders in 30 days (heavy zero inflation, skewed tail).
(b) Expected: RFM scoring, k-means on RFM, BG/NBD plus Gamma-Gamma, zero-inflated/hurdle regression, gradient boosting on 90-day value, Gini/decile lift, calibration.
(c) Very common.

### R3 Membership
(a) Zomato Gold relaunch Jan 2023 at Rs 149 for 3 months; 9 lakh members in a month (company claim); Flipkart Plus Silver 15 and Gold 25 transactions in 365 days; SuperCoin 1 or 2 per Rs 100, caps 50 per month and 15 per order. Unverified snippet figures (Gold about 30% to 40% of food GOV, about 60% frequency uplift) should be labelled as such if used.
(b) Expected: selection-bias handling (PSM, DiD, synthetic control), holdout/ramp, survival/churn modelling, contribution-margin economics, breakeven analysis.
(c) Common.

### R4 Coupons / budget allocation
(a) Meituan: 200+ features; AUC 0.891; PCOC 0.971 to 0.982; City B price x CVR 2.15 vs 2.09 (+2.8%); PID keeps price within about 1% of target (vs about 3% without); 50 ms decision latency.
(b) Expected: uplift modelling (T-learner, X-learner, causal forest), calibration, constrained optimisation / Lagrangian knapsack, cannibalisation analysis, A/B with budget guardrails.
(c) Very common.

### R5 Push / CRM
(a) Meesho: roughly 20 to 30 notifications per day; uninstalls unaffected; retention "stayed strong"; content, volume and time of day personalised. No percentages public.
(b) Expected: send-time optimisation (per-user open-hour histograms, contextual bandits), uplift on notification, frequency capping and fatigue/unsubscribe survival analysis, long-run holdouts.
(c) Very common.

### R6 Attribution / MMM
(a) Honasa: MMM plus geo-lift; no numbers public. Use only qualitative framing; simulation parameters (adstock, saturation) must be assumed and labelled as assumed.
(b) Expected: Bayesian MMM with adstock and Hill saturation, geo-experiment/difference-in-differences or synthetic control for incrementality, calibration of MMM using lift tests, MTA vs MMM trade-offs, last-click bias.
(c) Common.

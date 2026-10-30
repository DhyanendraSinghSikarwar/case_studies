# Book 6 — Part 1: Product Metrics and Metric Drops

**Topic:** Scenario-based product-metrics questions for Data Scientist, Product Analyst and ML Engineer loops at Indian product companies, GCCs and global tech: DAU, WAU and MAU drops, conversion, retention and revenue drops, one metric up while another is down, Simpson's paradox and mix shift, metric definition and instrumentation changes, seasonality and holidays, new versus existing users, platform, version and geography breakdowns, notification, ranking and pricing changes, success metrics for a new feature, north-star and guardrail metrics, funnel and cohort diagnosis, decomposition trees, SQL-flavoured follow-ups at concept level, and AI-era twists (metrics for a GenAI feature).

**Target:** 55  |  **Actual:** 55 (⭐⭐⭐ 18, ⭐⭐ 25, ⭐ 12)  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part owns diagnosing and defining metrics in product settings. It does not repeat the experiment theory in Book 1 Part 10 (choosing primary and guardrail metrics for a test, the Simpson's paradox definition inside an A/B test, reading a test where the primary metric and a guardrail disagree); the questions here are the same ideas met as live business situations (a dashboard drop, a rollup, a launch review), so Wave B answers should cross-reference those Book 1 questions only by checked headings. Book 6 Part 4 owns ambiguous experiment situations; Book 3 owns the full SQL; Book 2 owns GenAI internals (here only the metrics of a GenAI feature). All numbers in the prompts are invented illustrative numbers, not data from any company. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part01_sources.md). Searches returned metric-drop and root-cause question banks (Interview Query, Prachub, Codemia), product-sense and north-star pages (Dataford, datainterview.com), Simpson's-paradox prompts, metric trade-off guides, a checkout-conversion case page, Indian analyst interview guides (Interview Query, AmbitionBox, Dataford) and GenAI-chatbot metric posts. No result tied a single scenario to a named employer, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked as editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 Daily active users fell 10% over two weeks (8.2% in the latest week). The dashboard shows 1.00 million DAU two weeks ago, 0.98 million last week and 0.90 million this week, with no release notes anywhere. Walk through how you would find out whether the drop is real and what caused it, and what you would check in the first hour.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Success metrics for a new bill-splitting feature in a UPI payments app. The product team wants to know after four weeks whether it worked. Name the north star, two or three input metrics, and two guardrails, and say which one you would put in the launch review.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Pick a north-star metric for a food-delivery app and defend it. Candidates the team floated are orders per week, GMV, weekly active ordering users and 4-week repeat rate. Choose one, add two guardrails, and say what each rejected candidate would hide.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 The DAU to MAU ratio (stickiness) fell from 0.30 to 0.26 while MAU stayed flat at 20 million. Explain what this tells you that a DAU or MAU chart alone would not, and list the three or four hypotheses you would test first.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 Weekly orders on an e-commerce app fell 20% in the week after a big sale ended, compared with the sale week. Leadership asks if this is a problem. Explain how you would tell a normal post-sale hangover from a real decline, and which baselines you would compare against.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Android checkout conversion dropped from 3.1% to 2.6% while iOS is flat, starting the day version 8.4 shipped, while the crash rate is flat. Describe how you would narrow the cause, what you would compare by app version, and how you would decide between a product bug and a measurement bug.
**Asked at:** Funnel and checkout-conversion case pages (a Prachub Amazon checkout-conversion root-cause page, funnel guides from Amplitude, Hackle and Datadog); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 DAU rose 5% after a feature launch but total time spent per day fell 8%. A PM calls it a win because the headline is DAU. Explain how both can be true, what additional cuts you would run, and how you would decide whether this is good or bad for the product.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 A notification experiment sends more pushes to the treatment group: sessions per user rise 6% and DAU rises 2%, but 30-day uninstalls rise from 1.2% to 1.5% and notification opt-outs double. Decide whether to ship, which metric is the goal and which is the guardrail, and what extra analysis you want.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Day-7 retention for the last three weekly signup cohorts is 18%, 17% and 14%, versus a steady 20% earlier. Explain how you would separate a true product regression from a change in who is signing up, and which cohort cuts you would build.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Average order value on a grocery app fell 15% quarter over quarter, from Rs 520 to about Rs 442, while order count rose 9%. Is this bad? Show how you would decompose the change and decide which part, if any, needs action.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Overall conversion went from 4.0% to 3.8% this month, yet conversion rose on both mobile (from 2.0% to 2.2%) and desktop (from 6.0% to 6.2%). Explain how that is possible with a small worked example of traffic shares, and what you would tell the exec who only read the headline number.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Revenue is down 8% versus last month. Build a decomposition tree from revenue down to the leaf drivers you would query (for example users, conversion, orders per buyer, price and mix), say which branches you would test first and why, and how you would stop when you have found the cause.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Orders reported by the client-side checkout_complete event are up 4%, but finance's order table shows flat orders, and the conversion dashboard (built on the event) looks healthy. Explain how you would decide which number to trust, where the gap could come from, and what you would fix first.
**Asked at:** Funnel and checkout-conversion case pages (a Prachub Amazon checkout-conversion root-cause page, funnel guides from Amplitude, Hackle and Datadog); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🔴 The company redefined 'active user' in the middle of the quarter, from any app open to any open followed by a meaningful action, and the new dashboard shows MAU down 14% overnight. Explain how you would report the quarter honestly, rebuild a comparable series, and what you would say to an exec who wants to know if the business shrank.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🔴 A 12% drop in orders is concentrated in one metro city and started on a Tuesday. The city had heavy rain, a competitor discount, and a local delivery-partner strike in the same week. Describe how you would separate the explanations and quantify each, and what data you would need beyond your own logs.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🔴 A ranking change in the home feed lifts click-through rate 7% in the experiment, but orders per user are down 1.5% and cancellations are up. Explain how this can happen, which metric should decide, and how you would check the long-run effect before rolling out.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🔴 You launch a GenAI shopping assistant in the app. Define the funnel from exposure to success, the north star, quality and safety metrics, and the cost metric. Include what you would measure when a user asks a question and then leaves without clicking, and why standard click-based metrics can mislead here.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🔴 Average revenue per user (ARPU) fell from Rs 112 to Rs 104 company-wide, but ARPU rose in every one of the three countries you operate in. Show with a small numeric table how a mix shift produces this, how you would split the change into a within-country effect and a mix effect, and what you would report.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 Define 'active user' for a ride-hailing app and for a B2B analytics tool, and explain why the two definitions should differ. For each, say what action qualifies, over what window, and which fake-activity cases you would exclude.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 A retention curve for a new app flattens at 12% after day 30, while a competitor's guide quotes a higher plateau. Explain what a flattening curve means, what you would compare (cohorts, channels, definitions) before concluding anything, and what a curve that never flattens would imply.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 The order cancellation rate on a delivery app rose from 4% to 6% over two weeks. List how you would break it down (who cancels, at what stage, for what reason) and which one or two cuts would most quickly separate a supply problem from a customer problem.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 A funnel for a lending app shows visit to signup 40%, signup to KYC 55%, KYC to approval 70%, approval to disbursal 80%. Disbursal volume fell 10% month over month. Explain how you would find which step changed, and why step conversion and absolute counts need to be read together.
**Asked at:** Funnel and checkout-conversion case pages (a Prachub Amazon checkout-conversion root-cause page, funnel guides from Amplitude, Hackle and Datadog); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 Define success metrics for a referral programme that gives Rs 100 to both sides. List the metrics, the guardrails, and the abuse patterns, and say which number you would present to finance to prove the programme is not just buying users who leave.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 Email open rate jumped from 20% to 45% overnight with no change in content. Explain what you would suspect first, how you would check it using downstream metrics such as clicks and conversions, and what you would do to the metric definition.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 DAU fell 6% during the week of a major festival and a cricket tournament. Describe how you would test whether this is seasonal, which prior periods to line up (same festival last year, same weekday), and what you would say to a PM who wants an alert raised.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 New-user retention looks worse this month, but marketing shifted spend from organic and referral to paid social. Explain how channel mix can lower blended retention without any product change, and how you would report retention fairly across the mix shift.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 After a new OS release, DAU is down 5% only on iOS and only for users on the latest OS version. Describe the breakdowns, the logs and the checks you would use to decide between a real engagement loss and a tracking break, and who you would loop in.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 A delivery fee change raised the fee from Rs 20 to Rs 30 on small orders. Orders fell 6%, but revenue rose 4%. Say how you would judge whether the change was good, what guardrails and time horizon you would use, and which customers you would look at separately.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Subscription churn rose from 3% to 4.5% a month after a price increase. Describe how you would find which segments churned, tell price effects from the usual seasonality or a product issue, and estimate the revenue impact over the next year.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 In a two-sided marketplace, new seller listings grew 25% this quarter but buyer conversion fell from 5% to 4.2%. Explain the possible reasons, how you would tell a supply-quality dilution from a search or ranking problem, and which metrics you would add to monitor both sides.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 A new ETA model improved ETA accuracy by 15%, but orders in the treatment group are 2% lower. Explain how a better prediction can reduce orders, what you would look at by segment, and how you would pick the metric that decides the launch.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Sessions per DAU jumped 20% overnight while DAU stayed flat. Explain which causes you would test (bots, a logging change, a new auto-refresh, a real engagement spike), and which two checks would settle it fastest.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 A new onboarding flow lifts day-1 retention by 4 points, but day-30 retention is unchanged. Explain the likely story, how you would check for a novelty effect, and what you would recommend to the team that wants to ship it everywhere.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 The ads team raised ad load by one slot per feed, and ad revenue per user rose 9%, but app ratings fell and next-week sessions per user fell 2%. Explain how you would trade off the two, which horizon you would use, and what you would propose as the guardrail threshold.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 A push-notification cap of three per day is proposed. Describe the metrics you would use to judge the cap (goal, input and guardrail metrics), the segments where the cap might hurt most, and what result would make you reject it.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 Two teams report different MAU for the same month: 24.1 million versus 22.8 million. Explain the usual sources of such gaps (definition, deduplication across devices, time zone, bots, event source), and how you would reconcile them and prevent a repeat.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🔴 A daily metric is down 2% and an alert fired. The metric usually moves 1.5% day to day, with a weekend dip. Explain how you would decide whether this is noise, what baseline and interval you would use, and how you would set an alert that does not fire every Monday.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🔴 Conversion rate rose from 3.0% to 3.6% after a bot filter and a page-speed fix, but orders are flat. Explain how the denominator can change without the business improving, and how you would restate the metric so that the before and after periods are comparable.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🔴 A recommendation model refresh raised click-through rate by 5%, but catalogue diversity fell and 8-week retention in the treatment is down 0.5 point. Say how you would weigh a short-term lift against long-term harm, and what metrics and holdout you would set up to decide.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🔴 A quick-commerce tab inside a shopping app grew to 80,000 daily orders while the parent grocery tab lost 30,000. Explain how you would measure true incremental orders versus cannibalisation, and what you would report to leadership.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🔴 An LLM re-ranker is proposed for product search. Define the primary metric, a query-level ratio metric and guardrails (latency, zero-result rate, cost per query), and say what would worry you about the metric choice, for example sessions that end without a click because the answer was good.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🔴 GMV rose 30% in one month, but a growth analyst notices that a coupon code was used by a cluster of new accounts. Describe how you would test for promo abuse or fraud, which guardrail metrics you would have wanted in the launch review, and how you would restate the month.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🔴 The team wants to know if a new habit-forming feature improves 90-day retention, but the launch review is in three weeks. Explain how you would choose an early leading indicator, validate that it predicts 90-day retention, and state how much confidence it deserves.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟢 Build a baseline for an alert on daily active users that has a weekly cycle, a yearly festival pattern and steady growth. Explain how you would model the expected value, what you would do with holidays, and how you would pick the alert threshold.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟢 At concept level, describe how you would compute day-7 retention from a raw events table with user_id, event_time and event_name. Explain the grain, how you define the cohort day, the join back to events, deduplication, and what could silently inflate or deflate the number.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟡 At concept level, describe how you would write a query for week-over-week DAU by platform that does not lie. Cover the date spine for days with no events, window functions versus self-joins, timezone handling, and why partial current-week data distorts the last point.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 A daily dashboard shows a dip in the last hours of every day that fills in by the next morning. Explain how late-arriving events, time zones and batch loads cause this, how you would confirm it, and how you would change the reporting so no one raises false alarms.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 A publisher platform launches an AI summary box. Click-through to articles falls 18%, but time on site per session rises and satisfaction scores improve. Explain which metrics you would pick to judge the feature for users and for publishers, and what the guardrail should be.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 A GenAI assistant raised weekly task completions by 12%, but inference cost per active user doubled to Rs 6 a month. Explain how you would frame a unit-economics metric, what cost guardrail you would set, and how you would find the segment where the feature does and does not pay for itself.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 Retention is reported as the share of last month's active users who are active this month, and it rose from 55% to 62%. Explain how survivorship, resurrected users and a shrinking base could make this look good while growth is stalling, and what companion metrics you would add.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 For a group-chat product, the value of the app to one user depends on their friends being active. Explain how you would define engagement and success metrics when users are interconnected, why simple per-user averages can mislead, and what you would add to track network health.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 A notification team lifted push click-through rate by 25% using more urgent wording, and its own bonus is tied to that number. Explain how this metric can be gamed, which counter-metrics and holdouts would expose it, and how you would redesign the metric system so incentives line up.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 Revenue grew from Rs 100 crore to Rs 112 crore. Volume rose 6%, average price per unit rose 2%, and the mix moved toward a premium tier. Show how you would split the change into volume, price and mix effects with a small numeric table, state the assumption behind the order of the split, and explain what you would tell leadership.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 An AI support agent reports a 70% deflection rate (conversations not handed to a human), but complaints about the same issues are rising. Explain why deflection can overstate success, how you would measure true resolution with sampling and human labelling, and which guardrails you would add.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🔴 A platform-wide policy change (for example a new OS permission prompt) permanently resets a core metric's baseline in one week, so trend comparisons break. Explain how you would document the break, estimate what the metric would have been without it, and keep exec reporting honest for the next year.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

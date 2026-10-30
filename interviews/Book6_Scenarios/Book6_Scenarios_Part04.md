# Book 6 — Part 4: Experiment Design and Ambiguous A/B Results

**Topic:** Scenario-based "the A/B shows X, what do you do" questions for Data Scientist, Product Analyst and ML Engineer loops: sample ratio mismatch, novelty and primacy effects, peeking and sequential testing, multiple metrics, guardrails and multiple comparisons, underpowered or flat tests, minimum detectable effect and sample-size planning, network effects and interference, switchback and geo experiments, two-sided marketplace experiments, ratio metrics and the delta method, CUPED and variance reduction, heterogeneous effects and subgroup claims, Simpson's paradox inside experiments, contradictory metrics, ship or no-ship decisions on partial evidence, long-term holdouts and cumulative effects, bot and outlier contamination, logging and assignment bugs, when you cannot randomize (difference-in-differences, synthetic control, observational comparisons), bandits versus A/B tests, and AI-era twists (LLM feature tests, LLM-as-judge evaluation, non-determinism, silent model updates).

**Target:** 55  |  **Actual:** 55 (⭐⭐⭐ 18, ⭐⭐ 25, ⭐ 12)  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part owns the scenario, ambiguous-result and ship-decision angle (the data in front of you is messy, conflicting or suspicious; what do you do, in what order, with what evidence). It does not repeat the theory in Book 1 Part 10 (A/B testing, causal inference and experimentation); Wave B answers should cross-reference that part and Book 6 Parts 1 to 3 only by checked headings. Book 6 Part 2 owns models that degrade after launch and Part 3 owns imbalanced, noisy and missing data, so the object here is the experiment itself. All numbers in the prompts are invented illustrative numbers, not data from any company; every percentage names its base in the prompt and says whether it is a relative or absolute change, and every 'balanced' or 'significant' claim in a prompt is true of the numbers given. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part04_sources.md). Searches returned A/B-testing pitfall lists (Dataford, datainterview.com, PracHub), guardrail and ship-decision pages, marketplace, switchback and interference material (including a DoorDash careers post and an arXiv paper), ratio-metric and CUPED docs, causal-inference interview guides, underpowered-test articles, bot and outlier pages and 2026 practitioner posts on testing LLM features. Several searches returned general guidance rather than interview pages, and none tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A test meant to split 100,000 users 50/50 ended with 52,000 in control and 48,000 in treatment. Treatment shows conversion of 5.1% against 4.8% for control (0.3 percentage points absolute, about 6% relative to control's 4.8%) with p = 0.03, and the product manager wants to ship today. Explain what you check first and what you tell the manager.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 A test was planned for 14 days, and after 4 days the dashboard shows conversion of 6.3% in treatment against 6.0% in control (0.3 points absolute, 5% relative to control) with p = 0.03. The product manager wants to stop now and ship. Explain what is wrong with this and what you would do.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 A new button shows click-through rate of 5.6% in treatment against 5.0% in control in week 1, 5.3% against 5.0% in week 2 and 5.1% against 5.0% in week 3. The week-1 readout was already presented as a 12% relative lift. Explain what you think is happening, how you would confirm it and what number you would quote.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 A team reports 20 metrics for a test whose primary metric (purchases per user) is flat, and one secondary metric, time on page, is significant at p = 0.04, so the team calls the test a win. If none of the 20 metrics had a true effect and each were tested independently at the 5% level, the chance of at least one false positive would be about 64%. Explain how you would read this result and how the metrics should have been set up.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 A test with 40,000 users per arm shows conversion of 10.1% in treatment against 10.0% in control, and the 95% confidence interval for the absolute difference runs from about -0.3 to +0.5 percentage points. The product manager says 'no effect, kill it' while the designer says 'it is positive, ship it'. Explain what you conclude and what you recommend.
**Asked at:** Underpowered-test and MDE material (a Towards Data Science 'what to do when an A/B test result is not significant' article, a Dataford 'non significant test PM wants launch' page, a HackerNoon 'running A/B tests you can't measure' post, a Statsig power-analysis page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 A checkout redesign lifts conversion from 8.00% to 8.16% of visitors (+2% relative) while average order value among converters falls from 50.00 to 48.50 (-3% relative), and both changes are statistically significant. Explain how you decide whether to ship and which single metric you compute first.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 A feed ranking test raises sessions per user by 1.5% (relative to control) but also raises 95th-percentile page-load time from 1.00 to 1.08 seconds (8% relative), and the latency change is significant. The team's pre-registered rule allows at most a 5% relative degradation on that guardrail. Explain what you recommend and what you look at beyond the rule.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 A team measures click-through rate as total clicks divided by total impressions and runs a two-proportion z-test over 2,000,000 impressions per arm, getting p = 0.01 for a lift from 4.00% to 4.05%. Those impressions come from only 100,000 users per arm (20 per user on average), and the user-level analysis gives p = 0.12. Explain why the two disagree and how you would analyse the metric properly.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 A teammate says that because a user's pre-experiment spend has a correlation of 0.7 with their in-experiment spend, CUPED will cut the required sample size by 70%, and the test currently needs 100,000 users per arm. Explain whether the claim is right, what reduction you expect, and how you would choose and validate the covariate.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 In a test with 10,000 users per arm, control has 8,000 web users converting at 10% and 2,000 mobile users converting at 4%, while treatment has 2,000 web users converting at 11% and 8,000 mobile users converting at 5%. Overall conversion is 8.8% in control and 6.2% in treatment, so treatment loses overall although it wins in both segments. Explain what happened and what it says about the randomization.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 A messaging app tested a group-invite feature by randomizing 1,000,000 users 50/50, and treated users sent 20.6 invites per user against 20.0 for control (+3% relative to control). Control users who are friends with treated users also joined more groups. Explain what bias this creates, which way it pushes the measured lift, and how you would redesign the test.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Baseline conversion is 5.0%, and the team wants to detect a 5% relative lift (0.25 percentage points absolute) with 80% power at a two-sided 5% level, with 20,000 eligible visitors a day split evenly between two arms. The product manager wants a readout in 3 days. Explain what this test needs and what you say to the manager.
**Asked at:** Underpowered-test and MDE material (a Towards Data Science 'what to do when an A/B test result is not significant' article, a Dataford 'non significant test PM wants launch' page, a HackerNoon 'running A/B tests you can't measure' post, a Statsig power-analysis page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 A price change was launched in one city only. Orders per user per week in that city rose from 2.0 to 2.3 (+15% relative to its own baseline), while in five comparison cities the average rose from 2.0 to 2.2 (+10%) over the same weeks. Explain what effect you would estimate, what you assume, and how you would check the assumption.
**Asked at:** Causal-inference and when-you-cannot-randomize material (an Interview Query causal-inference guide on diff-in-diff and synthetic control, Codemia 'explain difference-in-differences' practice pages, NBER working paper 25532 on synthetic difference-in-differences); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 After a release, treatment shows 4% fewer add-to-cart events than control (relative to control), yet backend order counts are equal in the two arms. The release also renamed the add-to-cart event in the Android client, and Android is 45% of users. Explain how you diagnose this and what you do with the experiment.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 A test on 2,000,000 users per arm shows revenue per user up 0.4% relative to control, with a 95% confidence interval of +0.1% to +0.7%. Shipping costs 3 engineer-months and adds a feature to maintain, and the product manager says 'it is significant, so ship'. Explain how you make the decision.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🔴 A team looks at the experiment every day for 14 days and stops the first time p < 0.05, and an A/A simulation with that rule declares a 'winner' in roughly one run in five. Explain why, what you change in the process, and how you handle the business demand to be able to stop early.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🔴 A test with no overall effect (+0.3% relative to control, not significant) is sliced into 40 segments by country, device and tenure, and one segment, new Android users in one country, shows +9% relative with p = 0.01. If none of the 40 segment effects were real, the chance that at least one reaches p <= 0.01 would be about 33%. The product manager wants to launch for that segment, so explain what you do.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🔴 A test meant to split 1,000,000 users 50/50 has 495,000 in treatment and 505,000 in control. The treatment build crashes at launch on some older phones so those sessions never log events, treatment shows engagement per logged user up 2%, and the product manager says a 1% imbalance is small enough to ignore. Explain what is wrong and what the 2% means.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 An A/A test across 40 metrics shows 3 metrics with p < 0.05, and an engineer says the experimentation platform is broken. If every metric had no true difference and the tests were independent, about 2 of 40 would cross 5% by chance. Explain how you decide whether the platform is broken and what else you check.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 Treatment revenue is 1,060,000 against 1,000,000 for control (+6% relative to control) with 100,000 users per arm. Twelve treatment accounts with automated behaviour (thousands of page views a day) contribute 30,000 of the treatment revenue, and without them the lift is +3% relative. Explain how you decide on filtering, what you report, and how you keep such accounts out of future tests.
**Asked at:** Bot and outlier contamination material (Algolia engineering and docs pages on outliers in A/B tests, a Peakhour post on bots corrupting A/B data; the latter is vendor marketing); mostly practitioner pages, so scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 A page gets 4,000 users per arm per month with baseline conversion of 2.0%, and the product manager wants to detect a 5% relative lift (0.1 points absolute). That needs about 300,000 users per arm, or roughly 75 months at this traffic. Explain what you tell the manager and what alternatives exist.
**Asked at:** Underpowered-test and MDE material (a Towards Data Science 'what to do when an A/B test result is not significant' article, a Dataford 'non significant test PM wants launch' page, a HackerNoon 'running A/B tests you can't measure' post, a Statsig power-analysis page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 A food-delivery test ran Tuesday to Thursday (3 days) on 60,000 users per arm and shows a significant lift in orders per user. Weekend days account for about 40% of weekly orders and come with a different mix of customers. Explain whether three days is enough and how you choose the duration.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 A test compares one control with 4 treatment variants, each tested against control at the 5% level, and variant C wins with p = 0.03 while the other three are not significant. A Bonferroni threshold for 4 comparisons would be 0.0125. Explain how the extra variants change your read of C and what you recommend.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 A product manager randomizes each page view independently to the old or new checkout design, so one user can see both designs in one session, and reports 5.2% conversion per page view for new against 5.0% for old (+4% relative). Explain what is wrong with this randomization unit and how you would fix it.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 A test was randomized by device cookie, and 50,000 of 1,000,000 users (5%) turn out to appear in both arms because they use two devices. Treatment shows +2% relative lift among all users. Explain which way this contamination biases the result, how to measure it and what you would do about the readout.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 A ride-hailing app randomizes riders 50/50 for a discount, and treated riders take 5.5 rides per week against 5.0 for control (+10% relative to control). Pickup wait time for control riders rose from 4.0 to 4.4 minutes (+10% relative) compared with the pre-period, because treated riders absorb drivers. Explain what the measured lift represents and how you design a market-level readout.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 A social app wants to test a feed change with graph-cluster randomization, using clusters of about 50 users with an intra-cluster correlation of 0.02, and the user-level design needed 100,000 users per arm. The design effect is 1 + (50 - 1) x 0.02 = 1.98. Explain what this means for sample size, how cluster size trades bias against variance, and what you would do if traffic is limited.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 A delivery marketplace runs a switchback test on dispatch logic, flipping the whole market between old and new every 30 minutes for 14 days (672 periods, 336 per arm), with about 900 deliveries per period. An analyst computes a z-test on all 604,800 deliveries as if independent. Explain the right analysis unit, the carryover and time-of-day issues, and how you would randomize the periods.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 A brand campaign is tested by randomizing 20 regions 10/10, and the largest region, with 30% of total revenue (the other 19 hold about 3.7% each), landed in treatment. Explain what this does to the readout, how you would balance and analyse a geo experiment, and what you tell the marketing lead.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 In a UI redesign, existing users show sessions per day falling from 10.0 to 9.7 in week 1 (-3% relative to control), while new users (20% of traffic) show +4% relative. Explain how you separate a primacy effect from a real harm, how you test it, and how long you would run the experiment.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Revenue per user averages 20, with the top 0.1% of users contributing 25% of revenue, and a t-test shows treatment up 3% relative to control with p = 0.2 and a confidence interval wider than the effect. Explain your options for heavy-tailed metrics, what each trades away and how you would report the result.
**Asked at:** Bot and outlier contamination material (Algolia engineering and docs pages on outliers in A/B tests, a Peakhour post on bots corrupting A/B data; the latter is vendor marketing); mostly practitioner pages, so scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 A settings-page feature is seen by only 8% of users, and across all assigned users revenue per user is up 0.1% relative to control, not significant. Among users who reach the page, the lift is +1.25% relative. Explain how you analyse a test with low exposure, what the triggering rule must satisfy, and what you report.
**Asked at:** Underpowered-test and MDE material (a Towards Data Science 'what to do when an A/B test result is not significant' article, a Dataford 'non significant test PM wants launch' page, a HackerNoon 'running A/B tests you can't measure' post, a Statsig power-analysis page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 A team shipped 12 experiments over a year, each measured at about +1% on revenue, so adding them up gives about 12.7% (1.01 to the power 12). A long-term holdout group kept on the year-start experience shows +5.5% relative. Explain why the two differ and how you would report cumulative impact.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 A growth team wants a bandit rather than an A/B test to choose among 6 email subject lines for 600,000 recipients over 2 weeks, and then wants to claim a causal lift for next quarter's plan. Explain when a bandit is right, what you lose for inference and what you recommend.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 A search ranking change raises click-through per query by 5% relative to control but raises queries per session by 8% (users reformulating) and leaves purchases per session flat. Explain how you interpret these conflicting metrics and what additional metric or cut you would build before deciding.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 A support assistant with a new model raises the share of conversations resolved without a human from 60% to 63% (3 points absolute, 5% relative to control) in a user-level test, but the same user can get different answers to the same question on a retry. Explain how nondeterminism affects the design, which unit you randomize and what you measure besides resolution.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 An LLM judge prefers the new model in 620 of 1,000 offline pairs (62%), but humans agree with the judge on only 71% of 200 audited pairs, and the new model's answers are 35% longer. Explain how you validate the judge, what the 62% really tells you and how it connects to the online test.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 An LLM feature raises satisfaction by 2 points but also raises 95th-percentile latency from 1.4 to 3.1 seconds and cost per query from 0.002 to 0.012 dollars (6 times). Explain how you frame the ship decision, which guardrails and budgets you set and what you propose as the next experiment.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🔴 A booking platform gave a pricing tool to a random half of 10,000 hosts, and treated listings average 10.8 bookings a month against 10.0 for control listings (+8% relative to control). Guest demand in each city is roughly fixed, so the two groups compete for the same bookings. Explain what the +8% measures, what the market-level effect could be and how you design a test to estimate it.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🔴 Treatment raises sessions per user by 10% relative to control and lowers revenue per session by 4% relative to control, and the team reports 'revenue per session is down, so the test failed'. Revenue per user is therefore up about 5.6% relative to control (1.10 x 0.96 = 1.056). Explain which metric should drive the decision, why the ratio misleads here and what else you check.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🔴 A product launched in one country, and 15 other countries are available as donors. With 8 pre-launch weeks the synthetic-control fit has an average error of 1.5% of weekly revenue, and the post-launch gap is +2.5% of weekly revenue. Explain how you judge whether +2.5% is real using placebo tests, and what could invalidate the donor pool.
**Asked at:** Causal-inference and when-you-cannot-randomize material (an Interview Query causal-inference guide on diff-in-diff and synthetic control, Codemia 'explain difference-in-differences' practice pages, NBER working paper 25532 on synthetic difference-in-differences); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🔴 A teammate uses sessions during the first 3 days of the experiment as the CUPED covariate because it correlates 0.9 with the outcome (28-day sessions), and the adjusted confidence interval is much tighter. Treatment changes early sessions. Explain what is wrong, which direction the bias goes and what a valid covariate would be.
**Asked at:** Ratio-metric, delta-method and variance-reduction material (Spotify Confidence ratio-metric RFP and variance-reduction docs, MetricGate CUPED and delta-method pages, a TechPrep '66 Variance Reduction Interview Questions' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🔴 In an experiment with 100,000 users per arm the overall split is exactly 50/50, so the SRM check passes. By platform, control has 20,000 iOS and 30,000 Android users while treatment has 16,000 iOS and 34,000 Android users. Explain what this means, why the overall check missed it, and what you do with the result.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟡 A team ran 8 variants of a landing page against one control, picked the best (+4% conversion relative to control, p = 0.02) and shipped it, and a follow-up re-test of that variant alone shows +1.5% relative. Explain the winner's curse, how to estimate the true effect of the chosen variant and how you would design such tests.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 Two experiments run at once on the same users, one changing the recommendation carousel and one changing the carousel's layout, each randomized 50/50 independently, so 25% of users receive both treatments. Each is analysed alone and the combined group looks worse than either. Explain interaction effects, how to detect them and how platforms avoid them.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟡 In a redirect test, 100,000 users are assigned to each arm, but only 93,000 treatment users are logged as arriving on the new page against 100,000 in control. Treatment conversion among logged users is higher. Explain why this is a sample-ratio problem of a specific kind, what bias results and how you would recover a valid estimate.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 A Bayesian dashboard shows 'probability treatment is best' at 96% on day 5 of a planned 14-day test, and the team wants to stop. Explain whether peeking is still a problem under a Bayesian readout, what the 96% depends on and how you would set a stopping rule.
**Asked at:** A/B-testing pitfall guides (Dataford pages on pitfalls such as peeking, novelty effects, network interference and sample ratio mismatch, tagged in snippets to companies such as Lattice, Carvana and Arm; a datainterview.com A/B testing interview list; PracHub A/B testing topic pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 A retention offer was piloted in the 100 stores with the weakest sales last quarter, and their sales rose 12% relative to their own previous quarter while the all-store average rose 2%. Explain regression to the mean, why the 12% overstates the offer's effect and how you would redo the pilot.
**Asked at:** Causal-inference and when-you-cannot-randomize material (an Interview Query causal-inference guide on diff-in-diff and synthetic control, Codemia 'explain difference-in-differences' practice pages, NBER working paper 25532 on synthetic difference-in-differences); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 An LLM judge from the same model family as the treatment prefers treatment in 1,160 of 2,000 pairs (58%), while humans on 300 pairs prefer it 51% of the time. Explain self-preference and other judge biases, how you test for them and how you use the judge in an experiment.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 A ranking team says a user-level A/B test would need 6 weeks to detect a 0.5% relative lift in clicks, and proposes interleaving to get a result in 1 week. Explain why interleaving is more sensitive, what it cannot measure and when you would still run the A/B test.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 Leadership wants ship decisions after 7 days, but the target is 90-day retention, and across 60 past experiments the 7-day retention lift correlates 0.5 with the 90-day lift. Explain how you would build and validate a surrogate metric, what the 0.5 allows you to say and what long-term safeguards you keep.
**Asked at:** Guardrail and ship-decision material (a Dataford 'primary vs guardrail metrics' page, a Spotify Confidence guardrail-metric glossary and blog post, PracHub analytics-and-experimentation question pages, a Dataford 'non significant test PM wants launch' page); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 An ad-auction change is tested by randomizing advertisers 50/50, but treated and control advertisers bid for the same impressions and draw on shared budgets. Explain the interference, the bias in the naive comparison and how a budget-split or auction-level design would help.
**Asked at:** Marketplace, interference and switchback material (Dataford 'interference in marketplace experiments', 'marketplace experiment with interference' and 'choose switchback for marketplace dispatch' pages, a DoorDash careers blog post, an arXiv 2022 paper on switchbacks and interference bias, a Statsig marketplace-experimentation page); company practice is described only as the snippets reported it; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 Two weeks into a 4-week test of an LLM feature, the provider silently updated the underlying model, and a fixed 500-prompt regression suite run on the treatment path shows its pass rate moving from 82% to 87% (+5 points absolute) between week 2 and week 3. Explain how you detect and handle a mid-test change in the treatment and what you would pin or log in advance.
**Asked at:** AI-era experiment material (an Atlan 2026 guide to A/B testing LLM applications, tianpan.co 2026 posts on non-deterministic AI features, an efficientlyconnected.com post on nondeterminism); practitioner posts rather than confirmed interview banks, an emerging theme; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 Two experiments reuse the same hash salt, so of 100,000 users, 45,000 are in treatment of both, 5,000 in treatment of A only, 5,000 in treatment of B only and 45,000 in control of both. Each experiment looks balanced on its own. Explain how this contaminates both results, how you detect a bucketing collision and what you do with the readouts.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🔴 An uplift model ranks 1,000,000 users, the top 20% (200,000) get a coupon, and the team compares their conversion to the other 800,000 who got none and reports +15% relative. Explain why this does not validate the model, and how you would design a randomized evaluation with holdouts and an uplift curve.
**Asked at:** No public page found, editor-designed from the standard experimentation judgement themes that the guides above describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

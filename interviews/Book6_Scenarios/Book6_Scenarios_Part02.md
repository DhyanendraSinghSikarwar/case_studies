# Book 6 — Part 2: Model Performance Degraded in Production

**Topic:** Scenario-based "what do you do when..." questions for Data Scientist and ML Engineer loops on a model that gets worse after launch: accuracy, precision, recall or AUC falling, silent data, concept, label and prior drift, label delay and monitoring without labels, training-serving skew, feature-pipeline bugs and null or unit changes, upstream schema changes, feedback loops, seasonality, a model good offline but bad online, threshold and calibration decay, segment-level degradation, retrain versus rollback versus patch, shadow, canary and A/B validation of a fix, adversarial and fraud adaptation, recommender and ranking degradation, forecasting drift, and AI-era twists (LLM and RAG quality degradation, LLM-as-judge drift, agent tool changes).

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 16, ⭐⭐ 23, ⭐ 11)  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part owns the judgement angle (what do you do, in what order, with what evidence). It does not repeat the concept coverage in Book 1 (for example Part 1 on a model good offline but poor in production, Part 11 on training-serving skew, monitoring and retraining, Part 5 on drift and feedback loops in fraud, Part 6 on forecast monitoring) or the tooling in Book 4 Part 8 (drift tests, monitoring layers, late labels); Wave B answers should cross-reference those only by checked headings. Book 6 Part 1 owns product-metric drops (a business dashboard number fell); here the object is the model. Book 2 owns LLM internals, and here only the production-quality angle appears. All numbers in the prompts are invented illustrative numbers, not data from any company. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part02_sources.md). Searches returned production-degradation question banks (Dataford, Prepfully, TryExponent), MLOps and system-design guides on drift, skew and monitoring without labels, practitioner posts on fraud, calibration, schema changes, RAG degradation and shadow or canary rollout, and recommender feedback-loop papers. Forecasting-drift and adversarial-fraud searches found practitioner pages, not interview pages. No result tied a scenario to a named employer, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A fraud classifier launched with an offline AUC of 0.86 and a month later a labelled sample of 30,000 recent transactions gives an AUC of 0.79. Nobody has changed the model code. Walk through what you check first, in order, before deciding whether the model itself is at fault.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 A churn model flagged the top 5% of customers with 40% precision at launch, and three months later the same top 5% has 31% precision on newly matured outcomes. The retention team asks whether the model is broken. Explain what you would look at to separate a genuinely worse model from a change in who is being scored or how outcomes are recorded.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 A ranking model scored an offline AUC of 0.91 and was approved, but the live A/B test shows no lift in conversion. Your manager asks what could explain a model that is excellent offline and flat online. List the causes you would investigate and the order in which you would test them.
**Asked at:** Training-serving skew and offline-versus-online question pages (DesignGurus 'Grokking the AI System Design Interview', techinterview.org MLOps drift and feature-store guide, a Prachub ML-serving concept page); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 A card-fraud model launched two weeks ago, and chargeback labels arrive 45 to 60 days after each transaction, so no true label exists yet for anything it has scored. The approval rate and average score look normal on the dashboard. Explain how you would monitor whether the model is degrading during these first weeks, and what each signal can and cannot tell you.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 After an upstream deploy, the merchant_category feature's null rate jumped from 0.5% to 18% overnight, and a labelled check shows AUC falling from 0.88 to 0.84. The model still returns scores without errors. Explain how you would confirm the cause, what immediate action you would take, and how you would stop this class of failure going unnoticed again.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 A delivery-time model's mean predicted value rose from 28 to 41 minutes the day after a service release, while real delivery times did not change. The offline pipeline computes account_age in days and you suspect the service computes it differently. Explain how you would prove or disprove training-serving skew, and how you would fix it without retraining blindly.
**Asked at:** Training-serving skew and offline-versus-online question pages (DesignGurus 'Grokking the AI System Design Interview', techinterview.org MLOps drift and feature-store guide, a Prachub ML-serving concept page); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Model v2 went live five days ago and the headline business metric is down 4% versus the prior week, but the data distribution also shifted that same week because of a marketing campaign. Version v1 is still deployable. Explain how you would decide between rolling back, retraining and leaving v2 in place, and what evidence you would want inside 24 hours.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 A model's accuracy has been flat for a month: 89.6% overall, both before and after a change. Splitting by tenure shows existing users (80% of traffic) improved from 90% to 92% accuracy while new users (20% of traffic) fell from 88% to 80%. Explain why the aggregate hid this, what might cause the new-user drop, and how you would set up segment-level monitoring.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 A fraud team says precision at a fixed threshold fell from 67% to 50% and wants an emergency retrain. On a volume of 1,000,000 transactions the fraud rate fell from 1.6% to 0.8% over the same period, while recall (70%) and false-positive rate (about 0.56%) are unchanged. Explain what is actually happening, how you would check it, and whether a retrain or a threshold change is warranted.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 A loan-default model gets its true labels about 12 months after disbursal, and it has been live for six months. The business wants an early-warning system rather than waiting a year. Explain which signals you would build now, how you would use early repayment behaviour as a proxy, and how you would state your confidence honestly to risk leadership.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Weekly forecast error for an e-commerce demand model rose from a MAPE of 12% to 22% in the Diwali sale weeks, then returned toward 13% the week after. The data science lead asks whether the model has drifted. Explain how you would separate a predictable seasonal or event effect from real drift, and what you would change, if anything, in the model or its monitoring.
**Asked at:** No interview page located; forecast-monitoring practitioner pages (demandplanning.net MAPE and bias, John Galt Solutions, 42signals forecast-drift post) describe bias, structural breaks and MAPE blind spots, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Alerts show the population stability index (PSI) is above 0.25 for the age and city features, yet the model's labelled AUC is unchanged this month. A stakeholder wants an immediate retrain. Explain what the alert does and does not prove, which type of shift (covariate, prior, concept) you suspect, and how you would decide whether to act.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🔴 A loan-approval model was trained on past decisions and now only approved applicants ever produce repayment outcomes, so its own monitoring shows excellent default prediction on approved loans while losses on a new borrower segment rise. Explain how this feedback loop biases both retraining and monitoring, and what exploration, holdout or reject-inference options you would consider and their costs.
**Asked at:** Recommender feedback-loop and popularity-bias literature (Mansoury et al. 'Feedback Loop and Bias Amplification in Recommender Systems', a popularity-bias survey on arXiv) plus a Prachub ranking-debugging page; no public interview page for this exact prompt, so editor-designed from the literature; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🔴 A binary classifier's ranking quality is fine (AUC stable at 0.82), but predicted probabilities average 0.10 while the observed positive rate on matured data is 0.14, and a fixed 0.5 decision threshold now misses many positives. Explain how you would diagnose calibration decay, choose between recalibration, threshold change and retraining, and how often you would re-check it.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🔴 You have a retrained model that looks 1.2% better on a recent offline test set, and it will affect revenue-critical decisions. Explain how you would validate it through shadow mode, a canary and an A/B test, what each stage can and cannot show, which guardrails would trigger an automatic rollback, and how label delay changes the plan.
**Asked at:** Safe-rollout and shadow/canary guides (Qwak shadow-versus-canary post, Atlan shadow-deployment page, a NerdLevelTech MLOps-interview deployment-strategies lesson, a datainterview.com safe-rollout drill); commonly reported in public MLOps guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🔴 You discover a feature has been computed incorrectly for three weeks, so about 600,000 predictions made in that time may be wrong, and the logged feature values were also used to build this month's training data. Explain how you would contain the damage, decide which past decisions to re-score or revisit, and make sure the bug does not leak into the next retrain.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 A weekly dashboard shows model accuracy of 93.1% one week and 92.4% the next, each from 20,000 scored cases, and a manager asks if the model is degrading. Explain how you decide whether a change this size is signal or noise, and what monitoring design avoids both false alarms and missed slow declines.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 A support-ticket router's accuracy is stable, but the company has just launched a new product line that generates tickets with categories the model never saw. Explain what failure mode this is, how you would detect that such tickets are being misrouted, and what you would do in the short and long term.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 An engineer proposes retraining a pricing-support classifier every night so it never goes stale. Explain what you would check before agreeing, such as whether performance actually decays, the cost and risk of each retrain, and what you would want as a trigger instead of a blind schedule.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 An upstream team renamed a column and changed its type, and a default of 0 is now silently filled in where the model expects order_value in rupees. Labelled AUC falls from 0.85 to 0.82 over a week before anyone notices. Explain how you would find the cause quickly and what checks (schema, range, null, contract) would have caught it on day one.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 A recommender's click-through rate has slid 6% over eight weeks even though its offline NDCG improved 3% at launch. Catalogue diversity in recommendations has also shrunk. Explain how a feedback loop and exposure bias could cause this, how you would check for it, and what you would change.
**Asked at:** Recommender feedback-loop and popularity-bias literature (Mansoury et al. 'Feedback Loop and Bias Amplification in Recommender Systems', a popularity-bias survey on arXiv) plus a Prachub ranking-debugging page; no public interview page for this exact prompt, so editor-designed from the literature; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 A RAG support chatbot's thumbs-up rate fell from 78% to 69% in a week with no release from your team, and the LLM provider had pushed a silent model update. Explain how you would confirm the cause, what regression evidence you need from a fixed test set, and how to guard against provider-side change in future.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Answer quality in a RAG system dropped after the team re-embedded only the newly added documents with a newer embedding model, leaving the old vectors in the same index. Retrieval hit rate on a fixed query set went from 82% to 71%. Explain why mixing embedding versions hurts, how you would verify it, and how to fix and prevent it.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 A demand model that had a bias of about zero now over-forecasts by 15% after a competitor cut prices and the company changed its own pricing. MAPE has risen from 11% to 18%. Explain how you would diagnose a structural break, what you would do before you can retrain on enough new data, and how you would keep the business safe in the meantime.
**Asked at:** No interview page located; forecast-monitoring practitioner pages (demandplanning.net MAPE and bias, John Galt Solutions, 42signals forecast-drift post) describe bias, structural breaks and MAPE blind spots, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 A payments fraud model's catch rate on confirmed fraud fell from 85% to 70% over three months while its false-positive rate stayed flat, and analysts say fraudsters changed tactics. Explain how you would confirm adversarial adaptation, why naive retraining on recent flagged cases is risky, and which layered responses you would use.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 A search ranker's overall NDCG is stable, but long-tail queries (the 20% that are rare) have worsened by 8% while head queries improved. Explain how segment-level degradation can be hidden by head-query volume, how you would build a sliced evaluation and monitoring view, and what remedies exist.
**Asked at:** Recommender feedback-loop and popularity-bias literature (Mansoury et al. 'Feedback Loop and Bias Amplification in Recommender Systems', a popularity-bias survey on arXiv) plus a Prachub ranking-debugging page; no public interview page for this exact prompt, so editor-designed from the literature; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Mean score from a credit model fell from 0.30 to 0.22 this month, but outcomes will not mature for months. Explain the competing hypotheses (a change in applicants, a pipeline bug, a model change, real risk improvement), the checks that separate them using only unlabelled data, and what you would tell the business before labels arrive.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 A conversion model looks badly calibrated on the most recent seven days: predicted 5% against observed 1.5% for yesterday's cohort. The attribution window is seven days, so recent cohorts have not finished converting. Explain how label maturation creates this artefact, how you would restrict or adjust the evaluation, and why this matters for any alert threshold.
**Asked at:** Drift and monitoring-without-labels guides (techinterview.org MLOps guides, a DataDome write-up on monitoring models without labels, KodeKloud and NannyML-style material); commonly reported in public guides for MLOps and ML-system-design loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Revenue loss from a degraded risk model is about Rs 2 lakh per day, a proper retrain and validation takes two weeks, and a business-rule patch could be live tomorrow but is crude. Explain how you would weigh the patch against waiting for the retrain, what you would test about the patch, and how you would retire it later.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 A churn model trained before a major price change now shows weaker lift, since the relationship between usage and churn seems to have changed even though input distributions look similar. Explain why this is concept drift rather than data drift, how you would confirm it with labelled data, and what training-window and feature changes you would try.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 An ads click model's predicted-to-observed click ratio drifted from 1.00 to 1.12 over a quarter, meaning it over-predicts, while AUC barely moved. Explain why this matters for bidding, what might cause it (traffic mix, auction changes, feedback effects), and how you would recalibrate without retraining everything.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 A support-ticket triage LLM is checked weekly by humans on 400 random tickets, and accuracy went from 91% (364 of 400) to 86% (344 of 400) after a product launch. Explain whether that sample size supports calling it a real decline, what you would segment by, and how you would decide what to do next.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 A vision model that reads documents from phone photos has lost accuracy since a popular new phone with a different camera pipeline became common among your users. Explain how you would find this from the data, estimate its size, decide between augmentation, targeted data collection and a threshold change, and monitor for the next device shift.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 A summarisation feature's human rating slipped from 4.3 to 3.9 out of 5 after a developer edited the shared prompt template to fix one customer complaint, and neither the prompt nor the model version was recorded with each output. Explain how you would find out what changed, what a frozen regression set and prompt versioning would have shown, and how to ship prompt edits safely.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🔴 A model scored an AUC of 0.95 offline, but live AUC is 0.71. A review finds one feature was only populated after the outcome happened, so it leaked at training time but is empty at serving time. Explain how you would confirm leakage, quantify the damage, rebuild the evaluation to be point-in-time correct, and handle the live system while you fix it.
**Asked at:** Training-serving skew and offline-versus-online question pages (DesignGurus 'Grokking the AI System Design Interview', techinterview.org MLOps drift and feature-store guide, a Prachub ML-serving concept page); commonly reported in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🔴 A model trained on metro-city customers is launched in smaller cities and its precision falls from 62% to 48% in the new region, while the original cities hold steady. Explain how you would test whether covariate shift or a different relationship to the outcome is responsible, and whether you would reweight, add regional features, fine-tune or build a separate model.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🔴 A team retrained a model on the last four weeks of data and it performed worse than the old one. Those four weeks included a payment outage and a heavy promotion. Explain how training-window choice, unusual events and label quality could explain this, and how you would design the retraining dataset and validation to avoid repeating it.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🔴 A moderation model only gets true labels for items a human reviewer sees, which are mostly those the model already scored as risky. Reported recall has stayed at 90% while user reports of missed harmful content are rising. Explain the selection bias in the monitoring metric and how you would obtain an unbiased estimate, for example with random sampling.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🔴 In one week three things changed together: a model release, a large marketing campaign that brought in new users, and an upstream schema update. The conversion model's metric fell 5% and everyone blames a different cause. Explain how you would attribute the drop, which analyses and rollbacks you would use to isolate each cause, and how you would run the incident.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 A fraud model's decisions block flagged transactions, so only the flagged ones gain a quick label. Meanwhile its apparent precision rises over time while missed fraud found by other channels also rises. Explain how to run a small randomised exploration slice to measure the truth, how large it needs to be, and how you would justify its cost to the business.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 A classifier had a validation true-positive rate of 80% and a false-positive rate of 10%. In production without labels it flags 29% of cases as positive, where at training the positive rate was 20%. Explain how you would estimate the production prior under a label-shift assumption using the confusion-matrix approach, state the estimate, and say how you would then adjust the threshold or the model.
**Asked at:** Calibration, prior-shift and threshold-review material (an arXiv paper on calibrating metrics under class-prior change, a futureagi model-versus-data-drift post, a fraud-score vendor page on reviewing thresholds); no interview page for the exact scenario, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 A model's accuracy loses roughly 0.3 percentage points each week after training, each percentage point is worth about Rs 4 lakh per week, and a retrain costs Rs 6 lakh. Explain how you would model the cost of decay against the cost of retraining to choose a cadence, show the rough optimum, and name the assumptions (linear decay, constant stakes) that would break it.
**Asked at:** No interview question page located for this exact scenario; practitioner fraud and retraining guides (a Firstsource fraud-model post, a datainterview.com 'when to retrain' course page) describe the retrain-versus-rollback and adaptive-fraud themes, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 After a credit-scoring model was published and people learned what moves the score, applicants began gaming a few features and the score lost power. Explain this as performativity or Goodhart's law, how you would detect it, what features and monitoring are more robust, and how model transparency trades off against gaming risk.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 A shared embedding model was upgraded by the platform team, and three downstream models that consume its vectors each lost between 2 and 6 points of accuracy without any code change of their own. Explain the dependency chain problem, how you would detect it, and what versioning, contracts and canary practices the platform team should adopt.
**Asked at:** Upstream schema and silent feature-pipeline failure write-ups (Towards AI schema-migration post, RisingWave feature-pipeline observability, ActiveWizards Kafka schema-evolution post, dataexpert.io schema-drift post); practitioner posts rather than interview banks, so scenario is editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 A team monitors an LLM app with an LLM-as-judge that scored 4.2 last month and 4.5 this month, but a human spot-check of 100 outputs shows no improvement. Explain how the judge itself can drift or be biased, how you would calibrate it against human labels, and what governance you would put around automated quality scores.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 A tool-using LLM agent's task success rate fell from 82% to 74% after a third-party tool API changed its response format, and the failure was not visible in latency or error-rate dashboards. Explain how you would trace the failing step, what regression suite and contract tests would have caught it, and how to pick between prompt fixes, parsing fixes and fallback paths.
**Asked at:** AI-era RAG and LLM quality-regression guides (Braintrust RAG-observability article, Dataiku RAG-observability post, an Apptension RAG quality guide, practitioner posts on silent AI degradation); reported as a current theme in practitioner guides, not tied to a named employer; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 A retrained recommender showed a 3% conversion lift in week one of its A/B test, but the lift decayed to near zero by week four. Explain novelty effects, interference between buckets and cannibalised demand, how you would use a long-term holdout to settle it, and what you would tell the business about shipping.
**Asked at:** Safe-rollout and shadow/canary guides (Qwak shadow-versus-canary post, Atlan shadow-deployment page, a NerdLevelTech MLOps-interview deployment-strategies lesson, a datainterview.com safe-rollout drill); commonly reported in public MLOps guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 A company keeps 2% of traffic permanently on a frozen old model so it can measure model decay and the value of retraining, but finance says this costs about 2% of the model's revenue benefit. Explain the case for and against a permanent holdout, how you would size it, and cheaper alternatives for measuring decay.
**Asked at:** No public page found, editor-designed from standard production-ML judgement themes that the degradation guides describe in general terms; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 A regulation change in payments suddenly makes most of two years of transaction history unrepresentative, and only six weeks of new-regime data exists. Explain how you would keep a risk model running, which parts of the old data you would reuse, how you would use priors, simple models or human oversight in the interim, and how you would decide when to trust a new model.
**Asked at:** No interview page located; forecast-monitoring practitioner pages (demandplanning.net MAPE and bias, John Galt Solutions, 42signals forecast-drift post) describe bias, structural breaks and MAPE blind spots, so editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 A degraded model went unnoticed for three weeks and leadership wants a written account and a plan. Explain how you would structure a blameless postmortem for an ML failure, which detection and ownership gaps you would look for, how you would size the business impact, and what you would commit to as concrete monitoring and process changes.
**Asked at:** Production-degradation question banks (Dataford pages such as 'if a model's performance drops in production, what is your step-by-step diagnostic process', a Prepfully 'diagnose and fix a model deployed to production that underperformed' answer page, a TryExponent production-ML course page); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

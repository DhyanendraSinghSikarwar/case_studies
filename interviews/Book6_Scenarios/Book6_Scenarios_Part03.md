# Book 6 — Part 3: Imbalanced, Noisy and Missing Data Situations

**Topic:** Scenario-based "what do you do when the data looks like this" questions for Data Scientist and ML Engineer loops: extreme class imbalance (fraud, churn, rare disease), resampling, class weights, focal loss and their pitfalls (resampling before the split), metric and threshold choice (PR-AUC versus ROC-AUC), calibration after resampling, noisy and wrong labels and annotator disagreement, estimating label noise, missing-data mechanisms (MCAR, MAR, MNAR), imputation traps and leakage, missingness as signal, outliers versus errors, duplicates and near-duplicates across train and test, sampling bias and survivorship, small data, delayed, partial and positive-unlabelled labels, unit and encoding bugs, data-quality gates, subgroup under-representation, time-based and group splits, and AI-era twists (synthetic data, LLM-labelled data, weak supervision, model collapse).

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 16, ⭐⭐ 23, ⭐ 11)  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part owns the judgement angle (what do you do, in what order, with what evidence). It does not repeat the concept coverage in Book 1 (Part 3 on classification metrics, imbalance handling, resampling, thresholds and calibration; Part 2 on feature engineering and encoding); Wave B answers should cross-reference those and Book 6 Parts 1 and 2 only by checked headings. Book 6 Part 2 owns models that degrade after launch, and here the object is the data in hand. All numbers in the prompts are invented illustrative numbers, not data from any company; every percentage names its base in the prompt. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part03_sources.md). Searches returned imbalance and fraud-evaluation guides (techinterview.org, Dataford, KDnuggets), missing-data explainers, noisy-label research, leakage and duplicate guides, data-cleaning question banks, small-data prompts, data-quality-gate posts and AI-era labelling and synthetic-data papers. Positive-unlabelled, subgroup and label-noise estimation searches found research and practitioner pages, not interview pages. No result tied a scenario to a named employer, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A fraud dataset has 2,000,000 transactions of which 2,000 are fraud (0.1%), and a baseline that flags nothing scores 99.9% accuracy. Your manager asks why the new model's 99.8% accuracy should be seen as a failure rather than a near match. Explain what you would report instead and how you would split and evaluate the data.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 A colleague balanced a table of 10,000 rows (500 positives, 5%) to 50/50 with SMOTE and only then split it into train and test, and test recall came out at 0.93. After launch the recall measured on real traffic is 0.55. Explain what most likely went wrong and how you would redo the experiment.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 A model on a data set with 0.2% positives reports ROC-AUC 0.97 but PR-AUC only 0.18, and the stakeholder asks which number to believe. Explain what each metric measures here, what a no-skill model would score on PR-AUC, and what you would show the business.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 In a survey of 10,000 users, income is missing for 2,200 (22%). The missing share is 40% among the 4,000 users over 55 (1,600 users) and 10% among the other 6,000 users (600 users). Explain whether this looks like MCAR, MAR or MNAR, what you can and cannot test from the data, and what you would do before modelling.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 A churn model runs on 100,000 customers a month, of whom 4% (4,000) actually churn, and the retention team can only phone 2,000 customers a month. The data scientist proposes optimising F1 at the default 0.5 threshold. Explain which metric and threshold rule you would use instead and how you would report the expected result.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 You trained a gradient-boosted model on data with a 1% positive rate using a class weight of 99 on positives, and the mean predicted probability on a validation sample is about 0.50 although the true rate is 1%. Finance wants to use the scores as probabilities to compute expected loss. Explain what happened and how you would restore usable probabilities.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 In a loan dataset of 50,000 applications, income is missing for 15,000 (30%), and the default rate is 9% among applicants with missing income versus 4% among those who reported it. A teammate wants to fill the gaps with the median income and move on. Explain what you would investigate, how you would treat the missingness itself, and what could go wrong at serving time.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 A model trained on 40,000 rows from 8,000 customers (five rows per customer on average) was split randomly by row, and offline AUC is 0.95. On entirely new customers the AUC is 0.78. Explain how you would confirm the cause, how you would re-split, and how you would report the honest number.
**Asked at:** Duplicate and leakage guides (a DEV Community post on a train-versus-test dedup gain vanishing, a Voxel51 near-duplicate glossary page, DataEval and Arize leakage pages); commonly reported as a leakage theme in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 A churn model scores AUC 0.88 under a random split of twelve months of data, but 0.74 when trained on months 1 to 9 and tested on months 10 to 12. The product manager says the random-split number is the more reliable one because it uses more data for testing. Explain which number to trust, why the two differ and how you would set up validation.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Chargebacks take up to 60 days to arrive, and in the table of the latest 60 days the confirmed-fraud rate is 0.3% while older, fully matured months settle near 1.0%. An engineer wants to retrain weekly on the most recent three months. Explain what this does to the labels, how you would build a training set and an evaluation window, and what you would do about the recent weeks.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 In a payments table, 0.2% of rows have an amount above 1,000,000 rupees while the median amount is 800 rupees. Some of these are genuine corporate payments and some are entry errors with extra zeros. Explain how you would tell outliers from errors, what you would do with each group and whether you would clip, drop or keep them.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 A new partner feed covers 90,000 of 500,000 rows (18%) and reports distance in miles while the rest of the table is in kilometres, and nobody noticed until the delivery-time model's error rose. Explain how you would find the affected rows, how you would repair the data and the model, and which checks would catch this next time.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🔴 You trained a fraud model after keeping all 10,000 fraud rows and a random 10% of the 990,000 legitimate rows (99,000 rows, so 109,000 in all and a training fraud share of about 9.2%). A transaction gets a score of 0.50, and finance wants to use the scores as true probabilities for expected-loss calculations. Explain what the 0.50 means, how you would correct it to the 1% base rate, and how you would check the result.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🔴 A lender trained a default model only on the 60,000 approved applications from last year's 100,000, because the 40,000 rejected applicants never produced repayment outcomes. The model looks excellent on approved loans, but a new policy now lets in applicants who would previously have been rejected. Explain what bias this creates, what you would do about the rejected group, and how you would validate under the new policy.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🔴 A feature's missing values were filled with the mean target value within each city, computed on the whole data set before the split, and offline AUC is 0.93 against 0.71 live. The author says imputation cannot leak because it only uses a single column. Explain the leak, how you would prove it with an experiment, and how imputation should be set up instead.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🔴 After a vendor outage, a model feature that was missing in 5% of training rows was missing in 40% of live rows for two days, and live AUC fell from 0.83 to 0.74. The model uses mean imputation without a missing flag. Explain how you would diagnose this, what you would change in training and serving to make the model robust, and how you would alert on it.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 A data set of 60,000 rows has 300 positives (0.5%), and a tree ensemble takes two hours to train. A teammate suggests SMOTE, another suggests class weights, and a third suggests undersampling. Explain which you would try first, in what order you would compare them, and what metric you would compare them on.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Two annotators labelled 1,000 support tickets as urgent or not and agreed on 820 of them (82% raw agreement), and each marked about 30% of tickets as urgent. The team says 82% agreement is good enough. Explain what chance-adjusted agreement says here, what the disagreements suggest about the guidelines, and how you would form training labels.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 A table of 200,000 rows with 1,000 positives has 4,000 rows with a missing key feature, and 600 of those 4,000 rows are positive, against 400 positives among the other 196,000 rows. A manager says to drop the 4,000 rows because they are only 2% of the data. Explain why that is risky, what the numbers imply about the missingness, and what you would do instead.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 In a 300,000-row table, 12,000 rows (4%) hold -999 in the age column, and the income column is stored as text with entries such as 'N/A' and 'null' next to real numbers. A quick model is already trained and works acceptably. Explain how you would find and handle these sentinel and encoding problems, and how you would check whether they affect the model.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 A temperature sensor in a plant shows readings of 850 degrees Celsius for about a minute on 3 of 1,200 machines (0.25%), while normal readings run between 20 and 90. A teammate wants to winsorise them. Explain how you would decide between error and real event, what you would do in each case and what you would record for the downstream owners.
**Asked at:** Data-cleaning question banks (an Educative data-science interview data-cleaning lesson, a TechPrep '82 Data Cleaning Interview Questions' page, StrataScratch 'data cleaning traps', a DataCamp cleaning checklist) covering outliers versus errors and unit mismatches; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 A defect-detection image model has 300 defective images among 100,000 (0.3%), and a teammate wants to replace cross-entropy with focal loss. Another says that class weights are simpler. Explain when focal loss helps, what its parameters do, how you would compare it with the alternatives, and what calibration concerns you would raise.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 A screening test for a rare disease is applied to 20,000 patients with a prevalence of 0.5% (100 cases), and your model has sensitivity 90% and specificity 95%. Doctors say that 95% specificity sounds reliable. Explain what share of the positive flags would be true cases, how you would present that, and what you would change in the workflow.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 An LLM labelled 100,000 support tickets, and a human audit of 500 of them found that the LLM agreed with the humans on 440 (88%), with 45 of its 60 errors in the refund class. The team wants to train a classifier directly on the 100,000 labels. Explain whether and how you would use them, how you would size the audit, and how you would avoid fooling yourself in evaluation.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 A test set of 5,000 documents shows 300 exact matches with training (6%), but a MinHash near-duplicate check flags 1,550 (31%) of the test documents. The model's reported accuracy is 92%. Explain what this does to the reported number, how you would re-evaluate, and how you would stop it recurring.
**Asked at:** Duplicate and leakage guides (a DEV Community post on a train-versus-test dedup gain vanishing, a Voxel51 near-duplicate glossary page, DataEval and Arize leakage pages); commonly reported as a leakage theme in public guides; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 An app sent a satisfaction survey to 250,000 users and 10,000 replied (a 4% response rate), with a mean score of 4.4 out of 5 among responders. The team wants to train a model to predict satisfaction for all users from these responses. Explain what bias the sample probably has, how you would test for it and what you would do to correct or limit it.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 A credit model trained on 100,000 rows contains only 3,000 rural applicants (3%) but rural applicants are 8% of launch traffic, and the AUC is 0.84 overall but 0.71 for rural applicants. Explain how you would confirm and quantify the gap, what data or modelling steps you would try, and how you would decide whether to launch.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 A model with 400 labelled rows and 40 positives (10%) gives five-fold CV AUCs between 0.62 and 0.91, and the manager asks if the model is ready. Each fold holds 80 rows with 8 positives. Explain how you would quantify the uncertainty, which procedure you would use to choose a model, and what you would tell the manager.
**Asked at:** Small-data overfitting prompts (Dataford pages such as 'how do you handle overfitting in a model trained on small clinical datasets' and a high-dimensional few-samples prompt); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Only the 20,000 of 1,000,000 transactions (2%) flagged by old rules were reviewed by investigators, and 1,500 of them (7.5%) were confirmed as fraud, while the other 980,000 are treated as legitimate in the training table. The team wants to train a new model on this table. Explain what is wrong with the labels, how this is a positive-unlabelled problem, and how you would get an honest evaluation.
**Asked at:** Delayed-label, positive-unlabelled and selection-bias literature (Bekker and Davis PU survey, an arXiv paper on PU survival data, an arXiv paper on PU data under selection bias); no interview page for the exact prompt, so editor-designed from the literature; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 A nightly pipeline normally loads 5,000,000 rows, yesterday it loaded 3,100,000 (62% of the usual) and the model retrained on it without anyone noticing. You are asked to design data-quality gates. Explain which checks you would block on and which you would only warn on, how you would set thresholds, and what happens when a gate fails.
**Asked at:** Data-quality-gate material (a OneUptime 2026 data-pipeline validation post, a DesignGurus Great Expectations answer, an MLJourney post on quality checks for ML, a Pebblous Great Expectations report); practitioner posts rather than interview banks, so scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 A customer-level feature called spend_30d was computed with a window that sometimes extends up to 15 days after the prediction date, and the churn model's offline AUC is 0.91 against 0.77 live. The feature team says the window is just a rolling aggregate. Explain how you would prove the leak, how you would rebuild features with point-in-time correctness, and how you would check the rest of the feature set.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 A team has three heuristic labelling rules for spam that cover 20%, 35% and 50% of posts and often disagree where they overlap, and it has only 300 hand-labelled posts. They want to combine the rules into training labels. Explain how you would combine them, how you would estimate the accuracy of each rule, and what role the 300 hand labels should play.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 A team has 800 real fraud cases among 400,000 transactions (0.2%) and plans to generate 50,000 synthetic fraud rows with a generative model to make the data balanced. Explain the risks, how you would validate that the synthetic rows help rather than hurt, and why the test set must remain real data only.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 On a training set of 28,000 rows, a cross-validated model strongly disagrees with the given label (confidence above 0.95) on 700 rows (2.5%), and a reviewer finds that 62 of 100 sampled flagged rows are really mislabelled. Explain how you would estimate the overall label-noise rate, how far you would trust that estimate, and whether you would drop, relabel or down-weight those rows.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 A 12-class ticket classifier is trained on 100,000 tickets where the biggest class holds 40% and five classes each hold under 1,000 tickets. Overall accuracy is 91% but the team says the small classes are what the business cares about. Explain which metrics and averaging you would use, how you would handle the rare classes, and how you would report results.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 A test set holds 20,000 rows with only 20 positives, and the model catches 14 of them (recall 70%). The team wants to say recall is 70% and to compare it with an older model that caught 12. Explain how uncertain these figures are, how you would build the test set or compare the models, and what you would claim.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 A feature is missing in 15,000 of 100,000 rows (15%) and is strongly related to two other columns. The team debates median imputation, iterative model-based imputation and a tree model that handles missing values natively. Explain how you would choose between them, how you would judge imputation quality, and how you would keep imputation inside the cross-validation loop.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🔴 An audit of 2,000 random transactions with intensive investigation found 25 frauds, but only 20 of them carry a fraud label in the system, while the labelled fraud rate overall is 1%. Explain what kind of label noise this is, how it affects the training, the measured recall and the measured precision, and how you would estimate and handle it.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🔴 On a streaming app, users rate only about 2% of the titles they watch, the average rating among rated titles is 4.3, and a random prompt to 1,000 users gives an average of 3.6 on the titles they watched. A recommender is trained only on the observed ratings. Explain what missing-data mechanism is at work, how it distorts the model and how you would correct or evaluate for it.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 A team estimates that its crowd-sourced labels have asymmetric class-conditional noise: some true positives are labelled negative much more often than the reverse, and it has only 500 trusted labels. Explain how you would estimate the noise transition matrix, how you would use it to correct the loss, and where such correction breaks down.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 Dropping the 5% of 60,000 training rows with the highest loss (3,000 rows) raised validation accuracy by 1.0 percentage point, but accuracy for a dialect group that makes up 4% of the data (2,400 rows) fell, because 900 of the dropped rows belong to that group. Explain what the loss filter is really removing, how you would separate noise from hard but valid examples, and how you would check fairness of the cleaning step.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 A text corpus of 1,000,000 documents used for quarterly retraining now includes 600,000 documents generated by earlier versions of the model, so real data is 400,000 documents (40%). Quality metrics on a fixed real test set drift down each quarter. Explain what mechanism could be at work, how you would measure it, and what data policy you would set.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 A team labelled training data with one LLM and now uses the same LLM as the judge to measure whether the trained classifier is accurate, and the reported agreement is 96%. Explain the circularity, how you would build an independent evaluation set, and how you would measure and report the bias of the LLM labels by segment.
**Asked at:** AI-era LLM-labelling, weak-supervision and synthetic-data material (an arXiv 2026 abuse-detection paper using LLM annotators, an arXiv survey on LLM-driven synthetic data, an arXiv paper on weak data and model collapse, a Codemia labelling course page); emerging practitioner and research theme, not a confirmed interview staple; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 A model was trained on data imputed with an iterative multiple-imputation procedure that used the full data set, but at serving time a single request arrives with some fields missing and no other rows to borrow from. Explain why imputation for inference differs from imputation for prediction, how you would design serving-time handling, and how you would keep training and serving consistent.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 After a consent change, the share of 2,000,000 users with no tracked last_login rose from 8% (160,000 users) to 30% (600,000 users), and a retention model that used that feature degraded. Explain how the meaning of the missing value changed, what you would do about training data from before and after the change, and how you would handle it in the model.
**Asked at:** Missing-data interview explainers (a PrachHub 'Missing Data, Imputation, And Selection Bias' concept page, ydata.ai 'understanding missing data mechanisms', a Towards Data Science 'Talking About Missing Data' article, a Daily Dose of Data Science post on three types of missing values); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 An ad system sees 500 conversions in 50,000,000 impressions (1 in 100,000), and training on all rows is too costly, so the team keeps all conversions and 1% of non-conversions. Explain how this affects the calibration and the sampling variance of the model, how to correct the predicted probabilities for bidding, and how you would evaluate offline.
**Asked at:** Imbalanced-data and fraud-evaluation guides (techinterview.org 'Handling Imbalanced Datasets in Machine Learning', Dataford fraud-evaluation prompts such as 'how do you evaluate a fraud detection model on imbalanced data', a KDnuggets piece on SMOTE misuse, a Coresignal 'class imbalance interview trap' post); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 A retailer forecasts sales for 2,000 stores, of which 600 have under 30 weeks of history, and the global model does poorly on those small series. Explain how you would borrow strength across stores, what hierarchical or partial-pooling idea you would use, how you would validate on short histories, and when you would fall back to a simple rule.
**Asked at:** Small-data overfitting prompts (Dataford pages such as 'how do you handle overfitting in a model trained on small clinical datasets' and a high-dimensional few-samples prompt); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 A labelling vendor changed its guidelines, and the positive rate in the newest batch of 10,000 labelled rows is 12% against 8% in each of the previous six batches. The training pipeline ingested the batch automatically. Explain how a label-drift gate should work, how you would decide whether the shift is real or a guideline change, and what you would do with the batch.
**Asked at:** Data-quality-gate material (a OneUptime 2026 data-pipeline validation post, a DesignGurus Great Expectations answer, an MLJourney post on quality checks for ML, a Pebblous Great Expectations report); practitioner posts rather than interview banks, so scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 A medical imaging data set has 1,200 patients with six scans each (7,200 scans) and only 25 positive patients, and the team wants five-fold cross-validation. Explain why a plain stratified split by scan is wrong, how you would split by patient while keeping positives balanced (about five per fold), and how you would report the uncertainty of the result.
**Asked at:** Splitting and leakage guides (an arXiv paper on panel-data misuse of ML, a LetsDataScience 'science of data splitting' post, a Towards Data Science 'seven common causes of data leakage' article, an APXML recommender-splitting lesson); commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 Users flag 30,000 of 1,000,000 posts as harmful (3%), and a review of 500 randomly sampled flags found that 200 were fine. A model is trained on user flags as labels, and a coordinated group appears to be mass-flagging a topic. Explain how you would treat these labels, how you would detect coordinated flagging, and how you would measure the real precision of the flags.
**Asked at:** Noisy-label and annotator-disagreement material (Tanno et al., CVPR 2019 on annotator confusion matrices; a Codemia data-labelling course page); research and course pages rather than interview banks, so the scenario is partly editor-designed; search snippets only, not opened
<!-- ANSWER_PENDING -->

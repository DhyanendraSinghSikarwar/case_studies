# Book 6 — Part 6: Stakeholder Conflicts and Trade-off Decisions

**Topic:** Scenario-based "you and a stakeholder disagree, or two good options conflict; what do you do" questions for Data Scientist, Product Analyst and ML Engineer loops: a launch date the model cannot meet, business distrust of findings, accuracy versus latency versus cost versus interpretability, speed versus rigour under a deadline, ethics, fairness and privacy pushback, pressure to inflate or cherry-pick metrics, vague or shifting requirements, disagreeing with a senior person or an executive, saying no with data, backlog prioritisation, build versus buy politics, explaining a model to executives or regulators, owning a failed model or a wrong analysis, cross-team dependencies, resourcing disagreements, engineering versus data-science tension on productionising, ML versus rules baselines, dashboard versus model requests, black-box explanation demands, and AI-era twists (an LLM for everything, hallucination-risk acceptance, vendor API versus self-hosting, reviewing AI-written analysis).

**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 15, ⭐⭐ 20, ⭐ 10)  |  **Date:** 2026-10-30  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part keeps to trade-off decisions and stakeholder conflicts inside data-science and ML work, with numbers where a cost of delay, a threshold or an expected value can be computed. Generic behavioural scripts (conflict with a coworker, a time you failed, leadership stories) belong to Book 9 and are not repeated here; experiment theory belongs to Book 1 Part 10 and Book 6 Part 4, business case maths to Book 6 Part 5, and model degradation to Book 6 Part 2. Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers in one unnamed currency unit, not data from any company; every percentage names its base in the prompt, and every arithmetic claim in a prompt is checked in scratch/B6P06_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part06_sources.md). Searches returned Dataford, PracHub, codemia and Yardstick stakeholder-conflict and pushback prompt pages, trade-off guides, prioritisation and saying-no pages, ethics and explainability material, productionising pages and 2026 vendor and CTO posts on LLM build versus buy. Most results were user-contributed prompt pages or general guidance with few model answers; none tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A product manager has promised leadership a launch in 6 weeks, but your model needs 10 weeks to reach the quality bar. A rules baseline can ship in week 6 and captures 60,000 of the 100,000 weekly lift the full model would bring, and swapping in the full model would then slip to week 12. Compute cumulative lift by the end of week 12 for waiting and for the baseline-first plan, and say how you would present the choice to the PM.
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 A sales VP says your lead-scoring model is useless because ten leads he personally knows are strong scored in the bottom half. In your holdout the top-scored decile converts at 18% against 6% for all leads, which is 3 times the average. How do you respond in the meeting, and what do you offer to rebuild his trust?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 A bank's compliance team wants a logistic regression with reason codes for loan declines, while the data scientist prefers a gradient-boosted model. At a fixed 60% approval rate on 50,000 applications (30,000 approved), the logistic model approves loans with a 4.0% default rate and the boosted model 3.6%, and each default costs 2,500. Compute the defaults and loss avoided by the boosted model and say how you would settle the disagreement.
**Asked at:** Trade-off prompt pages (Dataford pages on accuracy versus interpretability and on accuracy versus latency and resource constraints, an Interview Query 2026 ML engineer guide that advises reasoning about interpretability versus performance and latency versus accuracy, Hyring and other 2026 guides that mention latency budgets and quantization); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 A ranking model A gives +1.2% relative click-through over model B, but its p95 latency is 80 ms against 25 ms for B and the product budget is 50 ms. A past latency test showed each extra 10 ms costs 0.3% of relative conversions, linear over this range. Compute the net effect of choosing A, assuming the click-through gain passes through to conversions one for one, and explain how you would decide with the ML lead and the product owner.
**Asked at:** Trade-off prompt pages (Dataford pages on accuracy versus interpretability and on accuracy versus latency and resource constraints, an Interview Query 2026 ML engineer guide that advises reasoning about interpretability versus performance and latency versus accuracy, Hyring and other 2026 guides that mention latency budgets and quantization); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 The CEO wants a revenue number for Friday's board deck, but you have just found that 3% of 200,000 order rows (6,000 rows) are duplicates, and cleaning and re-running takes two more days. The average order is 50, so gross revenue as currently computed is 10,000,000. What do you tell the CEO's chief of staff, and what exactly do you send by Friday?
**Asked at:** Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 A PM asks you to report the new onboarding's conversion using only logged-in visitors, which gives 3.5%, rather than all visitors, which gives 2.0%. Of 400,000 visitors 40% were logged in, and the 2.0% is across all of them. Work out the conversion for logged-out visitors and explain how you handle the request without damaging the relationship.
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 A director says she wants an AI that tells the team which customers are unhappy, with no definition of unhappy, no decision attached and a vague deadline of next quarter. You have one analyst and one engineer available. How do you turn the request into something you can build and measure, and what do you refuse to start until it is agreed?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Your tech lead wants a deep model for a routing task, but your gradient-boosted baseline reaches an AUC of 0.84 against 0.86 for his model. His model would cost 12,000 a month to serve and the baseline 1,500, a difference of 10,500 a month or 126,000 a year. How do you disagree with him in the design review, and what evidence would change your mind?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 A PM wants a personalised experience for a segment of 800 users a week, which gives 400 per arm, with baseline conversion of 5%, and expects a 0.5 percentage point lift. The standard error of the difference in a single week's conversion is about 1.5 percentage points. Say no with data, and propose what you would do instead.
**Asked at:** Prioritisation and saying-no prompt pages (many Dataford pages on prioritising competing stakeholder requests, a codemia page on saying no to a request, a Towards Data Science stakeholder-management article on declining requests and agreeing a start-now versus later list); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 The head of engineering wants to build a forecasting system in house, while finance wants to buy a vendor tool, and each side says the other is hiding costs. The build costs 900 up front plus 150 a year to maintain, and the vendor charges 400 a year, in thousands of one unit. Compute the 3-year cost of each, the break-even horizon, and the non-cost questions you would raise before recommending.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 A business owner says he cannot trust a model unless you tell him the exact rule behind each score. For one customer the churn probability is 17%, against a 10% base rate, and SHAP-style contributions are +6, +3 and -2 percentage points from three features. Show how you would explain this score, and say what you would not claim about the explanation.
**Asked at:** Explainability material (hirevire explainability pre-screening questions, fluxforce and other compliance-oriented pages on SHAP for regulators and model-risk guidance, a SHAP error-review workflow page); mostly vendor and practitioner pages rather than interview banks; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Four stakeholders each want a data-science project, and the team has 10 weeks of capacity. Project A is worth 280 (in thousands of one unit) and takes 6 weeks, B is worth 200 and takes 2, C is worth 150 and takes 3 and D is worth 120 and takes 5. Rank them by value per week, then find the best combination that fits in 10 weeks, and say how you tell the losers.
**Asked at:** Prioritisation and saying-no prompt pages (many Dataford pages on prioritising competing stakeholder requests, a codemia page on saying no to a request, a Towards Data Science stakeholder-management article on declining requests and agreeing a start-now versus later list); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🔴 A loan model approves 60% of applicants in group A and 42% in group B, a ratio of 0.7 against a four-fifths style screening heuristic of 0.8. The business head says the gap simply reflects different repayment risk and wants to ship this week. How do you test his claim, what options do you put on the table, and when do you escalate?
**Asked at:** Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🔴 Your demand model forecast 118,000 units for a month in which 100,000 were sold, and, if supply ordered to the forecast, the 18,000 excess units cost up to 25 each in markdowns and holding (450,000 at most). The supply-chain head is angry and asks in front of the group who approved the model. Say what you do in the first hour, the first week and the next quarter, including how you own your part.
**Asked at:** Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🔴 Leadership wants an LLM agent to answer every internal analytics question, and a pilot sample was 94% correct, which at 500,000 monthly questions projects 30,000 wrong answers. A wrong answer costs about 20 in rework or bad decisions, so that projects to 600,000 a month. How do you push back constructively, and where would you accept the risk versus add review?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 A marketing manager asks you for a churn model, but when you ask what decision it feeds she says she wants to see weekly churn by plan and region. A dashboard would take 2 weeks and a model about 10, five times as long. How do you handle the request, and when would you still build the model?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 The operations team defends a rule set that catches 60% of 2,000 monthly fraud cases, and your model catches 75% at the same 10% review rate. Each caught case saves 150, so the model catches 300 more cases for 45,000 a month. The ops lead worries about losing control of decisions, so how do you win him over without overselling?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Your launch is in 4 weeks, but the one feature your model needs is owned by a data-engineering team whose backlog is 6 weeks long. A proxy feature gives an AUC of 0.77 against 0.80 with the real feature and 0.74 without either. What do you ask the other team, and which launch plan do you propose?
**Asked at:** Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 An engineering manager says your notebook cannot go to production, and wants to rewrite it before launch. The nightly scoring of 2,000,000 rows takes 5 hours today (400,000 rows an hour) against a 2-hour limit, which needs 1,000,000 rows an hour. How do you handle the disagreement over who does what, and what do you agree before any rewrite starts?
**Asked at:** Productionising prompt pages (several Dataford pages on moving a model from a notebook to production and collaborating with a data engineer, a Martin Fowler article against running notebooks in production, PyData talks on the notebook-to-production friction); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Your manager must cut the data-science team from 6 people to 4 while requests keep growing. Each person has 10 person-weeks a quarter, 20% of which goes on meetings and support, so capacity falls from 48 to 32 person-weeks against a backlog of 72. How do you make the case for resourcing, and what do you offer to drop or defer?
**Asked at:** Prioritisation and saying-no prompt pages (many Dataford pages on prioritising competing stakeholder requests, a codemia page on saying no to a request, a Towards Data Science stakeholder-management article on declining requests and agreeing a start-now versus later list); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Product wants to launch an LLM summariser after an evaluation of 400 summaries found 12 with an unsupported claim, a 3% rate. The product lead says that is good enough, and the legal team has not been asked. How do you frame the uncertainty around the 3%, and how do you get a risk decision from the right owner?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 The platform team wants to self-host an open model, and you favour a vendor API for a feature that uses 3,000 million tokens a month. The API costs 0.60 per million tokens (1,800 a month) and self-hosting costs about 6,000 a month in fixed infrastructure. Compute the break-even volume, and say what other factors you would put in front of both sides.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 A junior analyst sends you an LLM-written summary saying revenue rose 12%, from 1,000,000 to 1,120,000, and the team is excited. Active users also rose 12%, from 50,000 to 56,000. Review the claim, and explain how you give feedback on the process rather than just the number.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 A compliance officer asks you to show why the credit model declined a specific applicant, but she distrusts SHAP because two retrains gave different top reasons for the same person. The model has 40 features and some are strongly correlated. How do you explain what the reasons mean, and what do you change to make them more stable?
**Asked at:** Explainability material (hirevire explainability pre-screening questions, fluxforce and other compliance-oriented pages on SHAP for regulators and model-risk guidance, a SHAP error-review workflow page); mostly vendor and practitioner pages rather than interview banks; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 The CEO asks why the churn model's precision is only 30 percent. It flags 1,000 customers, 300 of whom really churn, out of 100,000 customers with a 5% churn rate (5,000 churners), so recall is 6%. How do you explain these numbers to him, and what do you recommend he use them for?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 A PM has used three churn target definitions in one 20-day sprint, 30, then 60, then 90 days of inactivity, and each relabel-and-retrain costs you 3 days. The 9 days are 45% of the sprint (6 days, 30%, if the first build was planned work). What do you do about it, and how do you stop it happening again?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Marketing wants to use customers' location history in a propensity model, which would add 0.4 percentage points of conversion across 1,000,000 customers, or 4,000 extra conversions worth 20 each (80,000). The privacy team says the consent terms do not cover this use. How do you weigh the 80,000 against the risk, and what do you propose?
**Asked at:** Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 A team ran a test with five metrics and wants to headline whichever one is significant. With five independent metrics and no true effect, the chance of at least one significant result at the 5% level is 1 - 0.95^5, about 22.6%. How do you push back, and what do you agree with them before the next test?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 The CEO believes the holiday campaign drove sales, which were 23 million against 20 million a year earlier, up 15%. Comparison regions that did not get the campaign grew 11%, so the expected figure is 22.2 million and the campaign accounts for 0.8 million. How do you tell her that the campaign was worth much less than she thinks?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 After launch, a model drifts and nobody knows who gets paged: engineering says it is a data-science issue and data science says it is an infrastructure issue. The model has already run for 9 days with a degraded input feed. How do you settle ownership, and what do you propose for alerts and on-call?
**Asked at:** Productionising prompt pages (several Dataford pages on moving a model from a notebook to production and collaborating with a data engineer, a Martin Fowler article against running notebooks in production, PyData talks on the notebook-to-production friction); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Removing a postal-code feature cuts AUC from 0.80 to 0.78 but shrinks the approval-rate gap between two groups from 18 points to 6, a 12-point or two-thirds reduction. The credit-risk head only cares about AUC. How do you present the trade-off, and who should decide?
**Asked at:** Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 The growth team wants the feed model that maximises clicks, while the content team wants a model with more diverse creators. The diverse model costs 0.8% relative click-through (4.0% to 3.968%) and raises the share of impressions to small creators. How do you frame this for both teams, and what would you test?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Finance reports 4.2 million active users and the product team reports 3.6 million, a gap of 0.6 million or 14.3% of the finance figure, and each insists its number is right. The definitions differ on what counts as active and on how bots are treated. How do you resolve it in the room, and what do you change so it does not recur?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 The sales VP asks you to raise the quarterly forecast from the model's 10.5 million to the target of 12 million, a 1.5 million or 14.3% uplift on the model figure. He says the sales team will hit it with effort. How do you respond, and how would you represent the model, the target and the risk gap in the deck?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🔴 Your new model shows an AUC gain of 0.03 offline, but the online A/B test is flat after 3 weeks with a confidence interval that includes zero. The PM wants to ship anyway because of the roadmap, and you would rather stop. How do you handle the disagreement, and what do you check before you decide?
**Asked at:** Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟢 A stakeholder sets a target of 99% accuracy for a model on an event with a 1% base rate. A model that predicts no event for everyone already scores 99%. How do you reset the target without making the stakeholder feel foolish?
**Asked at:** Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 The model-risk team wants three more weeks of validation, and each week of delay costs about 25,000 in lost benefit, so 75,000 in total. The business head wants to skip some of the checks. How do you work with both, and what could you offer to shorten the review safely?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 Two data-science teams in different divisions built competing churn models, and each reports a slightly different AUC on its own data, 0.82 and 0.83. Executives want one model, and both team leads are defensive. How do you run a fair comparison, and how do you handle the politics?
**Asked at:** Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 The CFO asks the data-science team to justify its cost of 1.8 million a year. The team has claimed benefits of 3.0 million, but 40% of that is also claimed by other initiatives, so only 1.8 million is solely attributable. How do you present the return honestly, and what do you say about work whose value is hard to measure?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 Leadership proposes replacing the analytics team's routine requests with an LLM text-to-SQL tool. On a test of 200 representative questions it answered 148 correctly (74%), and the business says it needs 95% for unsupervised use. How do you present the result, and what hybrid arrangement would you suggest?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 A VP asks you in a planning meeting to commit to a 90% accuracy figure before anyone has looked at the data. You have not seen label quality, class balance or the baseline yet. What do you say in the meeting, and what do you commit to instead?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 You discover that a model presented to leadership last quarter had a leakage bug, and the reported AUC of 0.91 is closer to 0.78 once fixed. Decisions have been made on it and the senior sponsor would rather leave it quiet. What do you do and say, and in what order?
**Asked at:** Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 You are asked to retire a legacy scorecard that a powerful VP relies on, because your new model has an AUC 0.02 higher on a holdout, with a paired bootstrap interval that excludes zero. The VP's team built the scorecard and fears losing visibility and influence. How do you plan the transition, and what do you do if the VP refuses?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Legal, growth and trust-and-safety each want a different moderation threshold on 100,000 items with 2,000 true violations. Threshold X gives 60% recall at 80% precision and threshold Y gives 75% recall at 75% precision, and a missed violation costs 50 against 5 for a wrongly flagged item. Compute the cost of each, and say how you would get the three groups to agree.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Leadership says agentic AI will make the data-science team unnecessary within a year and asks for a plan to cut its scope. You believe parts of that are right and parts are risky. How do you frame the team's value, and which tasks do you volunteer to automate and which do you defend?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found
<!-- ANSWER_PENDING -->

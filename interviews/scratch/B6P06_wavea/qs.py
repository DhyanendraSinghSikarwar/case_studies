# Question data for Book 6 Part 6. Tuple: (stars, difficulty, scenario text, asked-key). All numbers are invented illustrative numbers.
import math, itertools
NS = "; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened"
ED = "No public page found for this exact scenario, editor-designed; the theme is adjacent to "
AS = {
 'S': "Stakeholder-conflict prompt pages (Dataford pages on a PM or business expert requesting something that conflicts with model limitations, on stakeholders disagreeing with your findings, on conflicting stakeholder feedback and on cross-functional conflict, plus codemia and Yardstick pushback and persuasion question pages)" + NS,
 'P': "Project-conflict prompts (PracHub pages on ML project milestones, scope and conflict, on stakeholder conflict under a compressed delivery timeline and on cross-functional pushback on an analysis; one is tagged to a large marketplace and one to a social platform on the page, unverified)" + NS,
 'T': "Trade-off prompt pages (Dataford pages on accuracy versus interpretability and on accuracy versus latency and resource constraints, an Interview Query 2026 ML engineer guide that advises reasoning about interpretability versus performance and latency versus accuracy, Hyring and other 2026 guides that mention latency budgets and quantization)" + NS,
 'R': "Prioritisation and saying-no prompt pages (many Dataford pages on prioritising competing stakeholder requests, a codemia page on saying no to a request, a Towards Data Science stakeholder-management article on declining requests and agreeing a start-now versus later list)" + NS,
 'E': "Ethics and fairness material (Yardstick data-ethics question page asking how bias was handled without disrupting the business, a University of Virginia online-ethics case on whether to keep a sensitive attribute in a model, a Data Science Newsletter ethics page, pre-screening pages on unethical data requests); practitioner pages rather than a confirmed interview bank" + NS,
 'W': "Productionising prompt pages (several Dataford pages on moving a model from a notebook to production and collaborating with a data engineer, a Martin Fowler article against running notebooks in production, PyData talks on the notebook-to-production friction)" + NS,
 'X': "Explainability material (hirevire explainability pre-screening questions, fluxforce and other compliance-oriented pages on SHAP for regulators and model-risk guidance, a SHAP error-review workflow page); mostly vendor and practitioner pages rather than interview banks" + NS,
 'A': ED + "AI-era build-versus-buy and hallucination-risk material (2026 vendor and CTO-guide pages such as ThirstySprout and TKMX AI on API versus self-host and LLM cost, an InfoQ LLM-adoption article); no interview page for the leadership-pressure framing was found",
 'N': ED + "stakeholder-management and trade-off prompt pages (Dataford and PracHub families) but no located page for this specific framing",
 'M': "Metric-definition and persuasion prompt pages (a 2026 data-analyst hiring guide naming a defended metric definition as a standard question, Yardstick persuasion and courage question pages for data scientists, Dataford pages on stakeholders disputing your findings)" + NS,
}
def wil(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
Q = []
def add(s, d, t, a): Q.append((s, d, t, a))

# ---------- 3 stars ----------
# Q launch date
assert 4*60000 == 240000
assert 2*100000 == 200000 and 6*60000 == 360000
add(3, '🟢', "A product manager has promised leadership a launch in 6 weeks, but your model needs 10 weeks to reach the quality bar. A rules baseline can ship in week 6 and captures 60,000 of the 100,000 weekly lift the full model would bring, and swapping in the full model would then slip to week 12. Compute cumulative lift by the end of week 12 for waiting and for the baseline-first plan, and say how you would present the choice to the PM.", 'S')
# distrust
assert 18/6 == 3
add(3, '🟢', "A sales VP says your lead-scoring model is useless because ten leads he personally knows are strong scored in the bottom half. In your holdout the top-scored decile converts at 18% against 6% for all leads, which is 3 times the average. How do you respond in the meeting, and what do you offer to rebuild his trust?", 'S')
# accuracy vs interpretability
assert 30000*0.04 == 1200 and 30000*0.036 == 1080 and 1200-1080 == 120 and 120*2500 == 300000
add(3, '🟢', "A bank's compliance team wants a logistic regression with reason codes for loan declines, while the data scientist prefers a gradient-boosted model. At a fixed 60% approval rate on 50,000 applications (30,000 approved), the logistic model approves loans with a 4.0% default rate and the boosted model 3.6%, and each default costs 2,500. Compute the defaults and loss avoided by the boosted model and say how you would settle the disagreement.", 'T')
# latency vs accuracy
assert round(55*0.03, 2) == 1.65 and round(1.2-1.65, 2) == -0.45
add(3, '🟡', "A ranking model A gives +1.2% relative click-through over model B, but its p95 latency is 80 ms against 25 ms for B and the product budget is 50 ms. A past latency test showed each extra 10 ms costs 0.3% of relative conversions, linear over this range. Compute the net effect of choosing A and explain how you would decide with the ML lead and the product owner.", 'T')
# speed vs rigour
assert 6000*50 == 300000 and 200000*50 == 10000000 and 300000/10000000 == 0.03
add(3, '🟡', "The CEO wants a revenue number for Friday's board deck, but you have just found that 3% of 200,000 order rows (6,000 rows) are duplicates, and cleaning and re-running takes two more days. The average order is 50, so gross revenue as currently computed is 10,000,000. What do you tell the CEO's chief of staff, and what exactly do you send by Friday?", 'P')
# inflate metrics
assert 400000*0.4 == 160000 and round(160000*0.035)==5600 and round(0.02*400000)==8000 and abs((8000-5600)/240000-0.01)<1e-9
add(3, '🟡', "A PM asks you to report the new onboarding's conversion using only logged-in visitors, which gives 3.5%, rather than all visitors, which gives 2.0%. Of 400,000 visitors 40% were logged in, and the 2.0% is across all of them. Work out the conversion for logged-out visitors and explain how you handle the request without damaging the relationship.", 'S')
# vague
add(3, '🟡', "A director says she wants an AI that tells the team which customers are unhappy, with no definition of unhappy, no decision attached and a vague deadline of next quarter. You have one analyst and one engineer available. How do you turn the request into something you can build and measure, and what do you refuse to start until it is agreed?", 'S')
# senior disagree
assert 12000-1500 == 10500 and 10500*12 == 126000
add(3, '🟡', "Your tech lead wants a deep model for a routing task, but your gradient-boosted baseline reaches an AUC of 0.84 against 0.86 for his model. His model would cost 12,000 a month to serve and the baseline 1,500, a difference of 10,500 a month or 126,000 a year. How do you disagree with him in the design review, and what evidence would change your mind?", 'S')
# say no
se = math.sqrt(2*0.05*0.95/400)
assert abs(se - 0.0154) < 0.0001
add(3, '🟡', "A PM wants a personalised experience for a segment of 800 users a week, which gives 400 per arm, with baseline conversion of 5%, and expects a 0.5 percentage point lift. The standard error of the difference in a single week's conversion is about 1.5 percentage points. Say no with data, and propose what you would do instead.", 'R')
# build vs buy
assert 900+150*3 == 1350 and 400*3 == 1200 and 900/(400-150) == 3.6
add(3, '🟡', "The head of engineering wants to build a forecasting system in house, while finance wants to buy a vendor tool, and each side says the other is hiding costs. The build costs 900 up front plus 150 a year to maintain, and the vendor charges 400 a year, in thousands of one unit. Compute the 3-year cost of each, the break-even horizon, and the non-cost questions you would raise before recommending.", 'N')
# black box
assert 10+6+3-2 == 17
add(3, '🟡', "A business owner says he cannot trust a model unless you tell him the exact rule behind each score. For one customer the churn probability is 17%, against a 10% base rate, and SHAP-style contributions are +6, +3 and -2 percentage points from three features. Show how you would explain this score, and say what you would not claim about the explanation.", 'X')
# backlog
items = {'A': (280, 6), 'B': (200, 2), 'C': (150, 3), 'D': (120, 5)}
best = max(sum(items[k][0] for k in c) for r in range(1, 5) for c in itertools.combinations(items, r) if sum(items[k][1] for k in c) <= 10)
assert best == 480
order = sorted(items, key=lambda k: -items[k][0]/items[k][1]); w = 0; v = 0
for k in order:
    if w + items[k][1] <= 10: w += items[k][1]; v += items[k][0]
assert v == 470 and order == ['B', 'C', 'A', 'D']
add(3, '🟡', "Four stakeholders each want a data-science project, and the team has 10 weeks of capacity. Project A is worth 280 (in thousands of one unit) and takes 6 weeks, B is worth 200 and takes 2, C is worth 150 and takes 3 and D is worth 120 and takes 5. Rank them by value per week, then find the best combination that fits in 10 weeks, and say how you tell the losers.", 'R')
# ethics
assert 42/60 == 0.7
add(3, '🔴', "A loan model approves 60% of applicants in group A and 42% in group B, a ratio of 0.7 against the common four-fifths guideline of 0.8. The business head says the gap simply reflects different repayment risk and wants to ship this week. How do you test his claim, what options do you put on the table, and when do you escalate?", 'E')
# failed model
assert 118000-100000 == 18000 and 18000*25 == 450000
add(3, '🔴', "Your demand model forecast 118,000 units for a month in which 100,000 were sold, and the 18,000 excess units cost 25 each in markdowns and holding. The supply-chain head is angry and asks in front of the group who approved the model. Say what you do in the first hour, the first week and the next quarter, including how you own your part.", 'P')
# LLM for everything
assert 500000*0.06 == 30000 and 30000*20 == 600000
add(3, '🔴', "Leadership wants an LLM agent to answer every internal analytics question, and a pilot answered 94% of 500,000 monthly questions correctly. A wrong answer costs about 20 in rework or bad decisions, so the 30,000 wrong answers cost 600,000 a month. How do you push back constructively, and where would you accept the risk versus add review?", 'A')

# ---------- 2 stars ----------
add(2, '🟢', "A marketing manager asks you for a churn model, but when you ask what decision it feeds she says she wants to see weekly churn by plan and region. A dashboard would take 2 weeks and a model about 10, five times as long. How do you handle the request, and when would you still build the model?", 'N')
assert 2000*0.60 == 1200 and 2000*0.75 == 1500 and 300*150 == 45000
add(2, '🟢', "The operations team defends a rule set that catches 60% of 2,000 monthly fraud cases, and your model catches 75% at the same 10% review rate. Each caught case saves 150, so the model catches 300 more cases for 45,000 a month. The ops lead worries about losing control of decisions, so how do you win him over without overselling?", 'N')
assert 6-4 == 2
add(2, '🟢', "Your launch is in 4 weeks, but the one feature your model needs is owned by a data-engineering team whose backlog is 6 weeks long. A proxy feature gives an AUC of 0.77 against 0.80 with the real feature and 0.74 without either. What do you ask the other team, and which launch plan do you propose?", 'P')
assert 2000000/5 == 400000 and 2000000/2 == 1000000
add(2, '🟡', "An engineering manager says your notebook cannot go to production, and wants to rewrite it before launch. The nightly scoring of 2,000,000 rows takes 5 hours today (400,000 rows an hour) against a 2-hour limit, which needs 1,000,000 rows an hour. How do you handle the disagreement over who does what, and what do you agree before any rewrite starts?", 'W')
assert 6*10*0.8 == 48 and 4*10*0.8 == 32
add(2, '🟡', "Your manager must cut the data-science team from 6 people to 4 while requests keep growing. Each person has 10 person-weeks a quarter, 20% of which goes on meetings and support, so capacity falls from 48 to 32 person-weeks against a backlog of 72. How do you make the case for resourcing, and what do you offer to drop or defer?", 'R')
lo, hi = wil(12, 400)
assert 0.017 < lo < 0.018 and 0.051 < hi < 0.053
add(2, '🟡', "Product wants to launch an LLM summariser after an evaluation of 400 summaries found 12 with an unsupported claim, a 3% rate. The product lead says that is good enough, and the legal team has not been asked. How do you frame the uncertainty around the 3%, and how do you get a risk decision from the right owner?", 'A')
assert 6000/0.60 == 10000
add(2, '🟡', "The platform team wants to self-host an open model, and you favour a vendor API for a feature that uses 3,000 million tokens a month. The API costs 0.60 per million tokens (1,800 a month) and self-hosting costs about 6,000 a month in fixed infrastructure. Compute the break-even volume, and say what other factors you would put in front of both sides.", 'A')
assert 1000000/50000 == 20 and 1120000/56000 == 20
add(2, '🟡', "A junior analyst sends you an LLM-written summary saying revenue rose 12%, from 1,000,000 to 1,120,000, and the team is excited. Active users also rose 12%, from 50,000 to 56,000. Review the claim, and explain how you give feedback on the process rather than just the number.", 'A')
add(2, '🟡', "A compliance officer asks you to show why the credit model declined a specific applicant, but she distrusts SHAP because two retrains gave different top reasons for the same person. The model has 40 features and some are strongly correlated. How do you explain what the reasons mean, and what do you change to make them more stable?", 'X')
assert 300/1000 == 0.3 and 0.05*100000 == 5000 and 300/5000 == 0.06
add(2, '🟡', "The CEO asks why the churn model's precision is only 30 percent. It flags 1,000 customers, 300 of whom really churn, out of 100,000 customers with a 5% churn rate (5,000 churners), so recall is 6%. How do you explain these numbers to him, and what do you recommend he use them for?", 'M')
assert 3*3 == 9 and 9/20 == 0.45
add(2, '🟡', "A PM has changed the churn target definition three times in one 20-day sprint, from 30 to 60 to 90 days of inactivity, and each change costs you 3 days of relabelling and retraining. The 9 lost days are 45% of the sprint. What do you do about it, and how do you stop it happening again?", 'S')
assert 1000000*0.004 == 4000 and 4000*20 == 80000
add(2, '🟡', "Marketing wants to use customers' location history in a propensity model, which would add 0.4 percentage points of conversion across 1,000,000 customers, or 4,000 extra conversions worth 20 each (80,000). The privacy team says the consent terms do not cover this use. How do you weigh the 80,000 against the risk, and what do you propose?", 'E')
assert round(1-0.95**5, 4) == 0.2262
add(2, '🟡', "A team ran a test with five metrics and wants to headline whichever one is significant. With five independent metrics and no true effect, the chance of at least one significant result at the 5% level is 1 - 0.95^5, about 22.6%. How do you push back, and what do you agree with them before the next test?", 'M')
assert round(20*1.11,6) == 22.2 and round(23-22.2, 1) == 0.8
add(2, '🟡', "The CEO believes the holiday campaign drove sales, which were 23 million against 20 million a year earlier, up 15%. Comparison regions that did not get the campaign grew 11%, so the expected figure is 22.2 million and the campaign accounts for 0.8 million. How do you tell her that the campaign was worth much less than she thinks?", 'M')
add(2, '🟡', "After launch, a model drifts and nobody knows who gets paged: engineering says it is a data-science issue and data science says it is an infrastructure issue. The model has already run for 9 days with a degraded input feed. How do you settle ownership, and what do you propose for alerts and on-call?", 'W')
assert 18-6 == 12 and (18-6)/18 == 2/3
add(2, '🟡', "Removing a postal-code feature cuts AUC from 0.80 to 0.78 but shrinks the approval-rate gap between two groups from 18 points to 6, a 12-point or two-thirds reduction. The credit-risk head only cares about AUC. How do you present the trade-off, and who should decide?", 'E')
assert round(4.0*(1-0.008), 3) == 3.968
add(2, '🟡', "The growth team wants the feed model that maximises clicks, while the content team wants a model with more diverse creators. The diverse model costs 0.8% relative click-through (4.0% to 3.968%) and raises the share of impressions to small creators. How do you frame this for both teams, and what would you test?", 'S')
assert 4200000-3600000 == 600000 and round(600000/4200000, 3) == 0.143
add(2, '🟡', "Finance reports 4.2 million active users and the product team reports 3.6 million, a gap of 0.6 million or 14.3% of the finance figure, and each insists its number is right. The definitions differ on what counts as active and on how bots are treated. How do you resolve it in the room, and what do you change so it does not recur?", 'M')
assert 12-10.5 == 1.5 and round(1.5/10.5, 3) == 0.143
add(2, '🟡', "The sales VP asks you to raise the quarterly forecast from the model's 10.5 million to the target of 12 million, a 1.5 million or 14.3% uplift on the model figure. He says the sales team will hit it with effort. How do you respond, and how would you represent the model, the target and the risk gap in the deck?", 'S')
add(2, '🔴', "Your new model shows an AUC gain of 0.03 offline, but the online A/B test is flat after 3 weeks with a confidence interval that includes zero. The PM wants to ship anyway because of the roadmap, and you would rather stop. How do you handle the disagreement, and what do you check before you decide?", 'S')

# ---------- 1 star ----------
assert 0.99*1000 == 990
add(1, '🟢', "A stakeholder sets a target of 99% accuracy for a model on an event with a 1% base rate. A model that predicts no event for everyone already scores 99%. How do you reset the target without making the stakeholder feel foolish?", 'M')
assert 3*25000 == 75000
add(1, '🟡', "The model-risk team wants three more weeks of validation, and each week of delay costs about 25,000 in lost benefit, so 75,000 in total. The business head wants to skip some of the checks. How do you work with both, and what could you offer to shorten the review safely?", 'N')
add(1, '🟡', "Two data-science teams in different divisions built competing churn models, and each reports a slightly different AUC on its own data, 0.82 and 0.83. Executives want one model, and both team leads are defensive. How do you run a fair comparison, and how do you handle the politics?", 'P')
assert round(3.0*(1-0.4),6) == 1.8
add(1, '🟡', "The CFO asks the data-science team to justify its cost of 1.8 million a year. The team has claimed benefits of 3.0 million, but 40% of that is also claimed by other initiatives, so only 1.8 million is solely attributable. How do you present the return honestly, and what do you say about work whose value is hard to measure?", 'N')
assert 148/200 == 0.74
add(1, '🟡', "Leadership proposes replacing the analytics team's routine requests with an LLM text-to-SQL tool. On a test of 200 representative questions it answered 148 correctly (74%), and the business says it needs 95% for unsupervised use. How do you present the result, and what hybrid arrangement would you suggest?", 'A')
add(1, '🟡', "A VP asks you in a planning meeting to commit to a 90% accuracy figure before anyone has looked at the data. You have not seen label quality, class balance or the baseline yet. What do you say in the meeting, and what do you commit to instead?", 'N')
add(1, '🔴', "You discover that a model presented to leadership last quarter had a leakage bug, and the reported AUC of 0.91 is closer to 0.78 once fixed. Decisions have been made on it and the senior sponsor would rather leave it quiet. What do you do and say, and in what order?", 'E')
add(1, '🔴', "You are asked to retire a legacy scorecard that a powerful VP relies on, because your new model has an AUC 0.02 higher on a holdout, with a paired bootstrap interval that excludes zero. The VP's team built the scorecard and fears losing visibility and influence. How do you plan the transition, and what do you do if the VP refuses?", 'N')
# moderation threshold
caught_a = 2000*0.60; fa = caught_a/0.9 - caught_a; cost_a = (2000-caught_a)*50 + fa*5
caught_b = 2000*0.80; fb = caught_b/0.7 - caught_b; cost_b = (2000-caught_b)*50 + fb*5
assert abs(cost_a - 40666.67) < 1 and abs(cost_b - 23428.57) < 1
add(1, '🔴', "Legal, growth and trust-and-safety each want a different moderation threshold on 100,000 items with 2,000 true violations. Threshold X gives 60% recall at 80% precision and threshold Y gives 75% recall at 75% precision, and a missed violation costs 50 against 5 for a wrongly flagged item. Compute the cost of each, and say how you would get the three groups to agree.", 'N')
add(1, '🔴', "Leadership says agentic AI will make the data-science team unnecessary within a year and asks for a plan to cut its scope. You believe parts of that are right and parts are risky. How do you frame the team's value, and which tasks do you volunteer to automate and which do you defend?", 'A')

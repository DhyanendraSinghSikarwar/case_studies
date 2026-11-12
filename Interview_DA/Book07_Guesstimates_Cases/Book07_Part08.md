# Book 7 — Guesstimates, Case Studies & Business Metrics | Part 8: HR/People Analytics Cases 🟡

**Target:** 50 questions | **Actual:** 57 questions
**Scope:** HR and people-analytics cases: attrition, hiring funnel, recruiting metrics, pay equity, workforce planning and diversity analysis, with inline numbers where a figure can be derived and structured diagnoses where it cannot.

### Q1 ⭐⭐⭐ 🟢 What is attrition rate, how is it calculated for a month, and how do you annualise it?
**Asked at:** commonly asked (no company-specific report found); HR-analytics question banks lead with it (unverified prep-site material).
**What the interviewer is checking:** Whether you know the formula, the right denominator (average headcount) and the two ways to annualise.
**Say this in the interview:** "Attrition is leavers divided by average headcount for the period. For a month I compute it that way, then either multiply by 12 for a quick annual figure or compound it for a more careful one."
**Definition in plain words:** Attrition rate is the share of your workforce that left in a period. Formula in words: people who left, divided by the average number of people employed, times 100. In symbols: Attrition % = Leavers / ((Opening + Closing) / 2) x 100.
**Worked answer:**
- Monthly: opening 480, closing 520 (illustrative), leavers 13. Average headcount = 500. Rate = 13 / 500 = 2.6%.
- Quick annualisation: 2.6% x 12 = 31.2%.
- Compounded: 1 - (1 - 0.026)^12 = 27.1%. It is lower because the pool of people who can leave shrinks as people go.
- Alternative: add up 12 months of leavers and divide by the 12-month average headcount; this is the cleanest annual figure.
**Result:** 2.6% a month, about 31% annualised (simple) or 27% (compounded).
**Check:** If every month were 2.6%, a year of leavers would be about 12 x 13 = 156 on a base of 500, i.e. 31.2%, which matches the simple method.
**Caveats:** One month is noisy (a batch of exits inflates it), so annualise only from a steady run of months. Decide whether to include voluntary only, interns, contractors, and retirements, and state it. Some firms divide by opening headcount; say which you use.
**Likely follow-ups:** 1) *Why average and not opening headcount?* Headcount changes during the period, and average matches the people actually exposed to leaving. 2) *Which annualisation do you prefer?* The trailing 12-month leavers over the average headcount, since it needs no assumption.
**Common mistakes / traps:** Dividing by closing headcount; multiplying a one-off bad month by 12 and presenting it as the annual rate; mixing voluntary with all exits without saying so.

### Q2 ⭐⭐⭐ 🟢 A company had 480 employees on 1 April and 520 on 30 April, and 13 employees left during April. What is the monthly attrition rate using average headcount?
Inline data: opening headcount 480; closing headcount 520; leavers in April 13.
**Asked at:** commonly asked (no company-specific report found); a standard HR-metrics calculation in prep-site question banks (unverified).
**What the interviewer is checking:** Clean arithmetic, the average-headcount denominator, and a sensible reading of the number.
**Say this in the interview:** "Average headcount is (480 + 520) / 2 = 500, so 13 / 500 = 2.6% for the month, roughly 31% if this pace held for a year."
**Definition in plain words:** Monthly attrition = leavers / average headcount x 100, where average headcount = (opening + closing) / 2.
**Worked answer:**
1. Average headcount = (480 + 520) / 2 = 500.
2. Attrition = 13 / 500 = 0.026 = 2.6%.
3. Context: headcount grew by 40 while 13 left, so about 53 people joined in April (40 net growth + 13 leavers).
**Result:** 2.6% for April. Annualised about 31.2% (x 12) or 27.1% compounded; treat as indicative only.
**Check:** Using opening headcount gives 13 / 480 = 2.7%; using closing gives 2.5%. The average sits between, as it should.
**Caveats:** One month only. A 8% jump in headcount in a month means hiring was heavy, so the new joiners are still "safe" in their first weeks, which flatters the rate.
**Likely follow-ups:** 1) *Is 2.6% high?* Depends on industry and role; compare with your own trend and a like-for-like benchmark. 2) *Would you split it?* Yes, voluntary versus involuntary and by tenure band.
**Common mistakes / traps:** Using only the opening 480; forgetting to state whether 13 includes involuntary exits; calling 31% "the annual attrition" without saying it is an extrapolation.

### Q3 ⭐⭐⭐ 🟢 What is the difference between voluntary and involuntary attrition, and between regretted and non-regretted attrition, and why do HR teams split the number this way?
**Asked at:** commonly asked (no company-specific report found); appears in HR-analytics question banks (unverified).
**What the interviewer is checking:** Whether you know one headline number hides very different stories, and that you can act on the split.
**Say this in the interview:** "Voluntary means the employee chose to go; involuntary means the company decided. Regretted means we wished we could have kept them. I split because each needs a different fix."
**Explain simply:**
- Voluntary attrition: resignations (better offer, career change, relocation, burnout). Involuntary: terminations for performance or conduct, layoffs, end of contract.
- Regretted attrition: a leaver the company wanted to keep (high performer, scarce skill, critical role). Non-regretted: low performers or roles the company was happy to lose.
- Why split: voluntary regretted exits are the costly, fixable ones (pay, manager, growth). Involuntary exits reflect hiring and performance processes. A flat 15% overall could be healthy (mostly non-regretted) or alarming (mostly regretted top performers).
- Mini example: 60 leavers = 40 voluntary + 20 involuntary. Of the 40 voluntary, 10 were top-rated. Report voluntary 40, regretted 10: retention effort goes to those 10 and their causes.
- Practice step: take any exit list, tag each row voluntary/involuntary and regretted/not, and compare tenure and manager patterns.
**Likely follow-ups:** 1) *Who decides regretted?* Usually the manager plus HR using rating, criticality and replacement difficulty; define the rule in advance so it is not biased after the fact. 2) *Is a high regretted rate always bad?* Yes, it signals a retention problem; a high non-regretted rate may just be healthy pruning.
**Common mistakes / traps:** Judging "regretted" after the person leaves with hindsight bias; treating all resignations as bad; ignoring involuntary exits that point to hiring-quality problems.

### Q4 ⭐⭐⭐ 🟢 What are time-to-hire and time-to-fill, and how do they differ?
**Asked at:** commonly asked (no company-specific report found); definitions appear across recruiting-metrics vendor blogs (unverified).
**What the interviewer is checking:** Whether you know the two clocks start at different points and can say what each is used for.
**Say this in the interview:** "Time-to-fill runs from the requisition being approved until the offer is accepted. Time-to-hire runs from the candidate entering the pipeline until acceptance. One measures the business's wait, the other the candidate's experience."
**Explain simply:**
- Time-to-fill: opening of the job requisition (or posting) to offer acceptance. Includes approval delays and sourcing time. It is the hiring manager's wait.
- Time-to-hire: when a specific candidate applied or was first contacted to their acceptance. It shows how fast the process moves a candidate.
- Definitions vary by firm (some end at joining date); always state start and end events.
- Mini example: a requisition opens 1 March, a candidate applies 20 March, accepts 5 April. Time-to-fill = 35 days (1 March to 5 April); time-to-hire = 16 days (20 March to 5 April). The 19-day difference is the time the role waited for its first applicant.
- Practice step: pull requisition-open and accept dates for last quarter, compute median for both.
**Likely follow-ups:** 1) *Mean or median?* Median, a few stuck roles skew the mean. 2) *Which to improve first?* Time-to-hire if candidates drop out; time-to-fill if roles stay vacant and cost output.
**Common mistakes / traps:** Using the two terms as synonyms; not saying where the clock starts; reporting the mean with a few very old open roles.

### Q5 ⭐⭐⭐ 🟢 A recruiting team extended 40 offers last quarter and 31 candidates accepted. What is the offer acceptance rate, and what would you check if it fell from 85% the quarter before?
Inline data: offers extended 40; offers accepted 31; previous quarter rate 85%.
**Asked at:** commonly asked (no company-specific report found); offer acceptance rate is a standard recruiting metric in vendor guides (unverified).
**What the interviewer is checking:** Correct rate, awareness of small samples, and a structured list of causes.
**Say this in the interview:** "31 out of 40 is 77.5%, down 7.5 points from 85%. With only 40 offers that is about 3 candidates, so I would first check whether it is noise, then compare by role, offer size and competitor."
**Definition in plain words:** Offer acceptance rate = offers accepted / offers extended x 100.
**Worked answer:**
1. 31 / 40 = 77.5%.
2. At 85% the team would have had 34 acceptances (40 x 0.85), so 3 fewer people accepted.
3. Checks, in order: (a) is the drop spread across roles or in one role/location; (b) offered CTC versus market and versus the candidate's current pay (hike %); (c) time from final interview to offer (slow offers lose people); (d) decline reasons and who they joined; (e) recruiter or hiring-manager differences; (f) a change in sourcing mix.
**Result:** 77.5%, a fall of 7.5 percentage points.
**Check:** 31 + 9 declined = 40. 9/40 = 22.5% decline, up from 15% (6 of 40).
**Caveats:** Small base, so a swing of 3 people is not conclusive. Offers still pending at quarter end should be excluded or noted.
**Likely follow-ups:** 1) *How to tell if it is real?* Compare against several quarters or run a simple test on proportions. 2) *Is accepted the same as joined?* No, see offer-to-joining drop-outs.
**Common mistakes / traps:** Over-reading a 3-person change; blaming salary without data; counting pending offers as declines.

### Q6 ⭐⭐⭐ 🟢 Total recruitment spend in a year was INR 18 lakh (job-portal fees, agency fees, referral bonuses, recruiter travel) and the company made 45 hires. What is the cost per hire, and what costs might this figure leave out?
Inline data: total spend INR 18,00,000; hires 45.
**Asked at:** commonly asked (no company-specific report found); cost per hire appears in recruiting-metrics guides (unverified).
**What the interviewer is checking:** Simple division, plus knowing the difference between external and internal costs.
**Say this in the interview:** "INR 18 lakh divided by 45 hires is INR 40,000 per hire, but that covers only the out-of-pocket costs; recruiter salaries, hiring-manager time and onboarding are missing."
**Definition in plain words:** Cost per hire = total recruiting cost / number of hires. Total cost = external costs (portals, agencies, referral bonuses, travel, ads) plus internal costs (recruiter salaries, tools, interviewer time).
**Worked answer:** 18,00,000 / 45 = INR 40,000 per hire.
**Result:** INR 40,000 per hire on the costs given.
**Check:** 40,000 x 45 = 18,00,000. Correct.
**Caveats:** Leaves out recruiter and HR team salaries, applicant-tracking software, interviewer time, employer-branding spend, joining bonuses, relocation, onboarding and training, and the cost of vacant seats. An average also hides the mix: an agency hire may cost many times a referral hire, so split by source and by seniority.
**Likely follow-ups:** 1) *Is the average useful?* Only per source or role level. 2) *Fully loaded cost?* Add internal costs; it could be much higher than INR 40,000.
**Common mistakes / traps:** Calling INR 40,000 the "total cost of a hire"; dividing by offers or applicants instead of hires; comparing across companies with different cost definitions.

### Q7 ⭐⭐⭐ 🟢 A hiring funnel had 2,000 applications, 400 shortlisted, 120 interviewed, 30 offers and 24 joiners. Compute the stage-wise conversion rates and the overall application-to-joiner rate, and say which stage you would look at first.
Inline data: applications 2,000; shortlisted 400; interviewed 120; offers 30; joined 24.
**Asked at:** commonly asked (no company-specific report found); funnel conversion is a core recruiting-analytics theme (unverified).
**What the interviewer is checking:** Stage-wise percentages, an overall rate, and a reasoned choice of where to dig.
**Say this in the interview:** "Rates are 20%, 30%, 25% and 80%, overall 1.2%. I would look first at application-to-shortlist for volume efficiency, and at offer-to-join because it is the costliest loss."
**Definition in plain words:** Stage conversion = people reaching a stage / people in the previous stage. Overall = joiners / applications.
**Worked answer:**
1. Application to shortlist: 400 / 2,000 = 20%.
2. Shortlist to interview: 120 / 400 = 30%.
3. Interview to offer: 30 / 120 = 25%.
4. Offer to join: 24 / 30 = 80%.
5. Overall: 24 / 2,000 = 1.2%. Check: 0.20 x 0.30 x 0.25 x 0.80 = 0.012.
**Result:** 20%, 30%, 25%, 80%; overall 1.2% (about 1 joiner per 83 applications).
**Check:** The product of stage rates equals the overall rate (0.012).
**Caveats:** Low early conversion is normal; judge against your own history and role type. The first stage loses 1,600 people, so a small improvement in targeting the job post or screening criteria saves recruiter time. Offer-to-join loses 6 people after the whole cost has been spent, so a few points there are worth more per head. I would start with application-to-shortlist (is the sourcing off-target?), then offer-to-join.
**Likely follow-ups:** 1) *Why is 80% worrying?* Each lost joiner restarts the process. 2) *How to compare periods?* Same funnel for the previous quarter, by source.
**Common mistakes / traps:** Computing every rate off the 2,000 base; fixating on the lowest percentage without considering scale and cost; ignoring time lag between stages.

### Q8 ⭐⭐⭐ 🟢 What is the unadjusted gender pay gap, and how is it different from an adjusted (like-for-like) pay gap?
**Asked at:** commonly asked (no company-specific report found); pay-equity practice prompts cover this distinction (unverified).
**What the interviewer is checking:** That you know a raw gap is not proof of unequal pay for equal work, and an adjusted gap is not the whole story either.
**Say this in the interview:** "Unadjusted compares average pay of men and women across the whole company. Adjusted compares like with like, controlling for grade, job, location and tenure. The first shows where women sit in the structure; the second tests equal pay for similar work."
**Explain simply:**
- Unadjusted gap = (average men's pay - average women's pay) / average men's pay x 100. (Median can be used too.)
- Adjusted gap: compare within the same job, grade, location, tenure, usually through a regression of log pay with a female indicator and the controls.
- Example: if most senior roles are held by men, the unadjusted gap is large even if men and women are paid identically within each grade. The adjusted gap would be near zero, but the representation gap becomes the issue.
- Caution: controls such as grade may themselves reflect bias (for example, in promotions), so a small adjusted gap does not clear the company.
- Practice step: take any pay file, compute the raw gap, then compute the gap within each grade and compare.
**Likely follow-ups:** 1) *Mean or median?* Report both; the median is less affected by a few very high earners. 2) *Which do you show leadership?* Both, with the reasons for the difference.
**Common mistakes / traps:** Saying an unadjusted gap means unequal pay for equal work; saying an adjusted gap of zero means no bias; ignoring small groups.

### Q9 ⭐⭐⭐ 🟢 What is a compa-ratio? An employee earns INR 9 lakh a year and the midpoint of their pay band is INR 10 lakh. What is the compa-ratio and how would you read it?
Inline data: salary INR 9,00,000; band midpoint INR 10,00,000.
**Asked at:** commonly asked (no company-specific report found); compa-ratio appears in pay-equity practice prompts (unverified).
**What the interviewer is checking:** Formula, reading, and judgement that a low ratio is not automatically unfair.
**Say this in the interview:** "Compa-ratio is actual pay divided by the band midpoint. 9 / 10 is 0.90, so this person is paid 10% below the midpoint of their band."
**Definition in plain words:** Compa-ratio = employee's pay / midpoint of the pay range for their grade. 1.00 means paid at the midpoint.
**Worked answer:** 9,00,000 / 10,00,000 = 0.90 (90%).
**Result:** 0.90, i.e. 10% below the midpoint.
**Check:** The midpoint is the reference; a person at 10,00,000 would be 1.00; at 11,00,000, 1.10.
**Caveats:** Roughly 0.80 to 1.20 is a common working range, but firms differ. A low ratio can be normal for a new joiner or someone recently promoted who is still growing into the role; it is a concern if it persists for strong performers or clusters by gender or group. Read it together with tenure, performance and time in grade.
**Likely follow-ups:** 1) *What is range penetration?* How far through the band min-to-max the pay sits. 2) *Use in pay equity?* Compare average compa-ratios by gender within a grade.
**Common mistakes / traps:** Treating the midpoint as a target for everyone; comparing compa-ratios across grades with different band widths without care.

### Q10 ⭐⭐⭐ 🟢 You are asked to analyse why employees are leaving. What data would you ask for, and what first cuts would you make?
**Asked at:** commonly asked (no company-specific report found); root-cause-of-attrition questions recur in people-analytics prep banks (unverified).
**What the interviewer is checking:** Structured data request, sensible first cuts, and awareness of confidentiality.
**Say this in the interview:** "I would define attrition first, then ask for a leaver and active employee file with tenure, role, manager, pay, rating and exit reasons, and cut by tenure, team, manager, pay position and performance."
**Explain simply:**
- Data to request: employee master (join date, exit date and type, department, grade, location, manager, age band, gender), pay (CTC, compa-ratio, last hike), performance rating, last promotion date, exit-interview tags, engagement survey scores, and market pay benchmarks. Keep the active population too, otherwise you cannot compute rates.
- First cuts: attrition rate by tenure band, department, location, manager, grade, pay position, rating, and time since last promotion. Compare against the active population, not only leavers.
- Look at who is leaving (regretted or not) before why.
- Triangulate exit-interview reasons with data: stated reasons are often polite ("better opportunity").
- Mini example: 40 leavers; 25 within 1 year of joining, so look at onboarding and hiring quality before pay.
- Practice step: build a pivot of leavers and headcount by tenure band and compute the rate in each.
**Likely follow-ups:** 1) *What if the data are messy?* Fix definitions and dates first. 2) *Cause or correlation?* The cuts show where, not why; follow with interviews and surveys.
**Common mistakes / traps:** Looking only at leavers' reasons; no denominators; reporting with names; skipping the data-definition conversation.

### Q11 ⭐⭐⭐ 🟡 Attrition at a 2,000-person IT services company rose from 14% to 21% over a year. Management asks you to find out why. How do you structure the diagnosis?
Inline data available: HRIS extract (join date, exit date, department, grade, location, manager, CTC, last rating, last promotion date), exit-interview tags, engagement survey scores, and market salary benchmarks.
**Asked at:** commonly asked (no company-specific report found); attrition diagnosis is the central HR-analytics case in prep banks (unverified).
**What the interviewer is checking:** A hypothesis tree, data cuts that split signal from noise, and recommendations tied to evidence.
**Say this in the interview:** "I would first confirm the rise is real and where it sits, then test four buckets: market pull, pay, manager and growth, and workload or hiring mix, and recommend targeted fixes for the biggest pocket."
**Clarify first:** Same definition in both years (voluntary only? contractors?). Is the 21% on average headcount? Any layoffs, acquisitions or policy changes? Is the rise broad or in specific pockets? Scale: 14% of 2,000 is about 280 leavers; 21% is about 420, so roughly 140 extra exits (at constant headcount).
**Structure:**
- Is it real? Definition, denominator, one-off events, batch exits.
- Where? Tenure, grade, department, location, manager, rating.
- Why (hypotheses): (1) market: demand surge and competitors paying more; (2) pay: compa-ratio and hikes below market; (3) career: long time since promotion; (4) manager and engagement: team-level scores; (5) workload, bench or project issues; (6) hiring mix: new joiners leaving early.
**What I would check, in order:** Attrition by tenure band and grade (pivot); regretted versus non-regretted by rating; compa-ratio of leavers versus stayers by grade; months since last promotion; team-level attrition versus engagement scores; exit-interview tags by cluster; top managers by attrition rate (with minimum team size).
**If the data shows...:** Increase concentrated in under-2-year tenure: onboarding and hiring quality. Concentrated in high performers with low compa-ratio: pay correction. Clustered under few managers: manager coaching. Broad across all with market benchmarks above internal pay: market-wide, adjust pay bands for critical skills. Long time since promotion: career-path review.
**Numeric work (if data given):** Excess exits about 140 versus last year at constant headcount; if 60% sit in one pocket (illustrative), that pocket is the first target.
**Recommendation:** Present the pockets and the evidence, propose 2 or 3 pilots (pay correction for critical skills, manager reviews, early-tenure programme), and track monthly attrition by pocket plus regretted exits.
**Likely follow-ups:** 1) *Correlation or cause?* Pilots and comparison groups test it. 2) *Cost?* Estimate replacement cost per exit to size the budget.
**Common mistakes / traps:** Jumping to "salary" without cuts; using only exit-interview reasons; ignoring that a hiring spurt changes tenure mix; no success metric.

### Q12 ⭐⭐⭐ 🟡 Using the tenure-band data below, compute attrition for each band and the overall figure, and say where you would focus a retention effort.
| Tenure band | Average headcount | Leavers in the year |
|---|---|---|
| Under 1 year | 300 | 87 |
| 1 to 3 years | 700 | 112 |
| 3 to 5 years | 600 | 54 |
| Over 5 years | 400 | 20 |
**Asked at:** commonly asked (no company-specific report found); tenure-band attrition is a standard first cut (unverified).
**What the interviewer is checking:** Rates by band, a correct overall rate (not an average of rates) and a focus argued from rates and counts.
**Say this in the interview:** "Under 1 year is 29%, 1 to 3 years 16%, 3 to 5 years 9%, over 5 years 5%, overall 13.65%. I would focus on the first year, then the 1 to 3 year band, which has the most leavers in the group beyond year one."
**Definition in plain words:** Band attrition = leavers in the band / average headcount of the band x 100.
**Worked answer:**
1. Under 1 year: 87 / 300 = 29.0%.
2. 1 to 3 years: 112 / 700 = 16.0%.
3. 3 to 5 years: 54 / 600 = 9.0%.
4. Over 5 years: 20 / 400 = 5.0%.
5. Overall: total leavers 273 / total average headcount 2,000 = 13.65%.
**Result:** 29%, 16%, 9%, 5%; overall 13.65% (about 13.7%).
**Check:** The simple average of the four rates is 14.75%, which is wrong because bands differ in size; the weighted result 13.65% is correct. Also 87 + 112 + 54 + 20 = 273.
**Caveats:** Under-1-year has the highest rate but 112 exits in the 1 to 3 band exceed 87. Rates guide where risk per person is highest; counts show where the volume is. People move between bands during the year, so average headcount by band is approximate. Compare with the previous year before concluding.
**Recommendation:** First priority: early-tenure retention (onboarding, buddy, 30-60-90 check-ins, hiring-fit review), because a 29% rate means roughly 3 in 10 new joiners leave. Second: career and pay review for the 1 to 3 band.
**Likely follow-ups:** 1) *Is a 29% rate surprising?* Early exits often point at hiring or onboarding quality. 2) *Next cut?* Source of hire, manager, and whether leavers were campus or lateral.
**Common mistakes / traps:** Averaging the four percentages; judging only by rate or only by count; ignoring that people change bands.

### Q13 ⭐⭐⭐ 🟡 Offer-to-joining conversion at a company fell from 80% to 60% in two quarters. How do you find out why?
Inline data available: per-offer records with offered CTC, hike percentage, notice period, source, recruiter, offer-date and joining-date, and reasons captured when a candidate drops out.
**Asked at:** commonly asked (no company-specific report found); offer drop-out analysis is a typical recruiting case (unverified).
**What the interviewer is checking:** Segmentation, separation of causes (offer quality, delay, competitor, candidate stage), and a decision-oriented recommendation.
**Say this in the interview:** "I would see where the 20-point fall is concentrated using the offer records: notice period, hike, source and recruiter, then read the drop-out reasons to see whether it is pay, a counter-offer or a long gap before joining."
**Clarify first:** Is joining measured on a fixed cut-off (offers made in a quarter and joined within X days)? Are open offers still within notice and wrongly counted as drops? Did the mix of roles, levels or locations change? Any policy change (offer approval time, joining bonus)?
**Structure:**
- Measurement: cohort definition, pending offers.
- Candidate side: long notice period (more time to get a counter-offer), low hike, competing offers.
- Company side: slow offer approval, weak follow-up between offer and joining, recruiter or manager differences.
- Mix: new sources, new role types.
**What I would check, in order:** Conversion by offer-quarter cohort with a fixed time window; by notice period band (0-30, 31-60, 61-90 days); by hike % band; by source; by recruiter; days from final interview to offer; drop-out reasons by category.
**If the data shows...:** Drop concentrated in 60-90 day notice: shorten with buy-outs or stay-warm engagement. Concentrated in low-hike offers: revisit offer bands. Concentrated in one source or recruiter: process or candidate-quality issue. Late-quarter offers still pending: measurement artefact, not a real fall.
**Numeric work (if data given):** On 100 offers, 80% means 80 joined; 60% means 60, so 20 more people lost per 100 offers, and each loss repeats the hiring cost. (Illustrative base of 100.)
**Recommendation:** Fix the biggest segment first (for example engagement programme for long-notice candidates), track conversion by cohort weekly, and report both acceptance rate and joining rate.
**Likely follow-ups:** 1) *What is a good joining rate?* Depends on notice periods and market; trend and segments matter. 2) *Quick wins?* Faster offers, regular contact between offer and joining.
**Common mistakes / traps:** Not fixing the cohort window; assuming pay is the reason; ignoring offers still in notice.

### Q14 ⭐⭐⭐ 🟡 Average time-to-hire rose from 32 days to 45 days. Using the stage durations below, locate the delay and suggest what to examine next.
| Stage | Average days, last year | Average days, this year |
|---|---|---|
| Application to screening | 4 | 5 |
| Screening to first interview | 8 | 9 |
| First interview to final interview | 9 | 14 |
| Final interview to offer | 5 | 8 |
| Offer to acceptance | 6 | 9 |
**Asked at:** commonly asked (no company-specific report found); stage-wise time analysis is a standard recruiting-analytics exercise (unverified).
**What the interviewer is checking:** That you add the stages, find each stage's contribution to the increase and say what to examine.
**Say this in the interview:** "The stages sum to 32 and 45 days, so the increase is 13 days. Most of it, 5 days, sits between the first and final interview, then 3 days each at the offer stage and the acceptance stage."
**Definition in plain words:** Time-to-hire here is the sum of average stage durations; each stage's delay = this year minus last year.
**Worked answer:**
1. Last year: 4 + 8 + 9 + 5 + 6 = 32. This year: 5 + 9 + 14 + 8 + 9 = 45.
2. Changes: 1, 1, 5, 3, 3 = 13 days.
3. Shares of the increase: first-to-final interview 5/13 = 38%; final to offer 3/13 = 23%; offer to acceptance 3/13 = 23%; the first two stages 2/13 = 15% combined.
**Result:** Total delay +13 days (+41%); the biggest contributor is first-to-final interview (+5 days, from 9 to 14, a 56% rise).
**Check:** 1 + 1 + 5 + 3 + 3 = 13 and 45 - 32 = 13.
**Caveats:** Averages hide outliers; check medians and the spread. Stages are summed from averages, which is valid for means if the same candidates pass every stage. Check mix change (more senior roles take longer).
**Recommendation:** Examine interview scheduling and panel availability (calendar waits), feedback turnaround after interviews, the approval chain for offers, and the gap between offer and acceptance (negotiation, counter-offers). Cut by role, hiring manager and recruiter.
**Likely follow-ups:** 1) *Does shorter always mean better?* No, quality and candidate experience matter. 2) *Where is the cheapest gain?* Feedback and scheduling delays.
**Common mistakes / traps:** Blaming the stage with the largest absolute time (screening to interview, 9 days) rather than the largest increase; using averages without medians.

### Q15 ⭐⭐⭐ 🟡 The average salary of men is INR 12.0 lakh and of women is INR 10.2 lakh in a 600-person company. What is the unadjusted gap as a percentage of men's pay, and how would you investigate whether it reflects unequal pay for equal work?
Inline data: average men INR 12.0 lakh; average women INR 10.2 lakh. Available columns: job family, grade, tenure, location, performance rating, prior experience.
**Asked at:** commonly asked (no company-specific report found); pay-gap investigation prompts appear in pay-equity prep material (unverified).
**What the interviewer is checking:** Correct percentage with the right base, and a plan separating composition effects from like-for-like gaps.
**Say this in the interview:** "The unadjusted gap is (12.0 - 10.2) / 12.0 = 15%. To test equal pay for equal work I would compare within job family and grade and then run a regression with those controls."
**Definition in plain words:** Unadjusted gap % = (men's average - women's average) / men's average x 100.
**Worked answer:**
1. Difference = 12.0 - 10.2 = INR 1.8 lakh.
2. Gap = 1.8 / 12.0 = 15.0%.
3. Women's average is 10.2 / 12.0 = 85% of men's. (Measured on women's pay the difference is 17.6%; note the base.)
4. Investigation: (a) count men and women by grade and job family, which shows whether women are concentrated in lower grades; (b) compare average pay within each grade and job family; (c) regress log salary on a female indicator plus grade, job family, tenure, location, performance and experience; (d) check the compa-ratio by gender; (e) look at starting pay and hike history by gender.
**Result:** Unadjusted gap 15% of men's pay (INR 1.8 lakh).
**Check:** If the within-grade gaps are about zero, the 15% is composition, a representation issue; if gaps persist within grade, it points to unequal pay.
**Caveats:** Controls such as grade and rating can themselves be biased. Small cells (for example 3 women in a grade) are unreliable; suppress or pool. Report the median too.
**Likely follow-ups:** 1) *Next step if adjusted gap exists?* Review individual cases and correct. 2) *Is 15% bad?* It needs the context of structure and trend.
**Common mistakes / traps:** Dividing by women's pay by accident; concluding discrimination from the raw gap; controlling away the very channels (promotion) where bias may sit.

### Q16 ⭐⭐⭐ 🟡 A regression of log salary on a female indicator plus grade, tenure, location and job family gives a coefficient of -0.04 on the female indicator (statistically significant). How do you interpret it and what would you report to leadership?
**Asked at:** commonly asked (no company-specific report found); log-salary regression for pay gaps appears in pay-equity prep material (unverified).
**What the interviewer is checking:** Interpretation of a log coefficient, honesty about limits, and a leadership-ready message.
**Say this in the interview:** "A coefficient of -0.04 on log salary means women earn about 3.9% less than comparable men after those controls, which is statistically significant, so I would report a small but real adjusted gap and recommend reviewing individual cases."
**Explain simply:**
- Log salary means the coefficient is roughly a percentage difference. Exact: e^(-0.04) - 1 = -3.9%.
- Holding grade, tenure, location and job family equal, women's pay is about 3.9% lower on average. "Significant" means unlikely to be chance, not that it is large.
- Example: for a comparable man at INR 10,00,000, the comparable woman is estimated at about INR 9,60,800.
- Limits: it does not prove discrimination (omitted factors such as performance or skills may matter); controls like grade may themselves carry bias; an average hides a few large gaps.
- Report to leadership: the adjusted gap (about 4%), the unadjusted gap with its drivers (so representation is not missed), a confidence interval, the rough rupee cost of closing the gap, and a plan: review outliers individually, fix starting pay and promotion processes, re-run annually.
- Practice step: re-run the model with and without grade to see how much of the gap sits in grading.
**Likely follow-ups:** 1) *Why log salary?* Effects are percentages, and pay is skewed. 2) *Would you add performance?* Test both ways, since ratings can be biased.
**Common mistakes / traps:** Reading -0.04 as INR 0.04 lakh or as exactly 4%; saying significant means large; claiming proof of bias.

### Q17 ⭐⭐⭐ 🟡 Of 100 people hired in January, 88 are still employed at 3 months, 76 at 6 months and 61 at 12 months. Compute the 12-month retention and the share of the remaining people lost in each interval, and say what pattern suggests.
Inline data: start 100; month 3: 88; month 6: 76; month 12: 61.
**Asked at:** commonly asked (no company-specific report found); cohort retention is a standard people-analytics exercise (unverified).
**What the interviewer is checking:** Retention versus interval loss rates, and noticing that the intervals have different lengths.
**Say this in the interview:** "12-month retention is 61%. Of those still there, 12% were lost in the first 3 months, 13.6% in months 3 to 6, and 19.7% in months 6 to 12, but the last interval is twice as long, so per month it is actually flat or slightly lower."
**Definition in plain words:** Retention at t = still employed at t / starting number. Interval loss = people lost in the interval / people present at its start.
**Worked answer:**
1. 12-month retention = 61 / 100 = 61%.
2. Months 0-3: 12 lost of 100 = 12.0%.
3. Months 3-6: 12 lost of 88 = 13.6%.
4. Months 6-12: 15 lost of 76 = 19.7%.
5. Per-month equivalent: about 4.2%, 4.8% and 3.6% a month (compounded).
**Result:** 61% retained; 39 of 100 gone; interval losses 12.0%, 13.6%, 19.7% (monthly about 4.2%, 4.8%, 3.6%).
**Check:** 100 - 12 - 12 - 15 = 61.
**Caveats:** Quarter-wise the losses look like they accelerate, but the last interval covers 6 months, so the true monthly pace is highest at months 3 to 6, a typical point when the probation ends or the first appraisal or bonus cycle arrives. The pattern means steady early churn across the year rather than a single cliff; it suggests onboarding, role expectations and a mid-first-year checkpoint. Also 100 people is a single cohort; compare with other cohorts and source.
**Likely follow-ups:** 1) *Which method would you use for more cohorts?* Survival curves (Kaplan-Meier). 2) *Action?* Check-ins at months 2 and 5, review hiring fit.
**Common mistakes / traps:** Dividing every loss by the original 100; comparing 3-month and 6-month intervals as if equal; ignoring cohort size.

### Q18 ⭐⭐⭐ 🟡 A company has 18% annual attrition. How do you decide whether that is high or low?
**Asked at:** commonly asked (no company-specific report found); benchmarking attrition is a common follow-up in HR-analytics rounds (unverified).
**What the interviewer is checking:** That you do not answer with a single number and consider benchmark, trend, composition and cost.
**Say this in the interview:** "18% alone says nothing. I would compare it with its own trend, similar companies in the same industry and role mix, and then look at who is leaving and what it costs."
**Explain simply:**
- Compare with: (1) own history (was it 12% or 25% last year); (2) peers, by industry, city and role type, with an assumed, unverified benchmark that you must source; (3) internal pockets: a company-wide 18% could hide 35% in one team and 8% elsewhere.
- Composition: voluntary versus involuntary, regretted versus not, early tenure versus late. 18% mostly of low performers may be healthy; 18% of top performers is not.
- Cost: replacement cost (hiring, ramp-up, lost output) per exit times leavers. Mini example: 1,000 people x 18% = 180 exits; at an assumed INR 3 lakh replacement cost each, about INR 5.4 crore.
- Business goal: a fast-growth or high-skill firm may tolerate more churn than a steady operations team.
- Practice step: build a one-page view with trend, peer figure, split and cost.
**Likely follow-ups:** 1) *Is zero attrition the goal?* No; some turnover brings fresh talent. 2) *What if no benchmark exists?* Use internal trend and pockets.
**Common mistakes / traps:** Quoting an industry average as fact without a source; ignoring composition; treating all exits as equally costly.

### Q19 ⭐⭐⭐ 🟡 How would you measure quality of hire, and what are the limitations of each proxy?
**Asked at:** commonly asked (no company-specific report found); quality of hire is discussed across recruiting-analytics guides (unverified).
**What the interviewer is checking:** That you offer several measurable proxies, combine them, and admit that none is perfect.
**Say this in the interview:** "There is no single measure; I would combine performance rating after 6 to 12 months, retention, manager satisfaction and time-to-productivity into one index, by source, and state each one's limits."
**Explain simply:**
- Proxies: (1) first-year performance rating (limit: rater bias and rating inflation, and small teams); (2) retention at 12 months (limit: leaving can reflect the manager or market, and staying is not the same as performing); (3) hiring-manager satisfaction survey (limit: subjective, halo effects, low response); (4) time to full productivity or ramp-up (limit: hard to measure in some roles; depends on role complexity); (5) promotion or internal mobility (limit: long lag, politics); (6) assessment score versus later performance (limit: validates the test only, and data exist only for those hired, which is range restriction).
- Combine: standardise each as a score, weight it by importance and average by role, then compare by source, recruiter or interviewer.
- Mini example: source A: retention 90%, average rating 3.8; source B: retention 70%, rating 3.9. A wins on retention, similar on performance.
- Limits overall: the lag (results come after a year), small samples, and only hired people are observed.
- Practice step: join hire records with 12-month rating and retention and compare by source.
**Likely follow-ups:** 1) *Which single proxy would you start with?* 12-month retention plus rating, since both exist in HR data. 2) *How to handle lag?* Use early indicators (30-90 day manager check) alongside.
**Common mistakes / traps:** Using retention alone; mixing ratings across teams with different rating habits; ignoring survivorship (only those who stayed have ratings).

### Q20 ⭐⭐⭐ 🟡 Which hiring source would you invest more in, based on the data below?
| Source | Applicants | Hires | Still employed at 12 months | Total cost (INR lakh) |
|---|---|---|---|---|
| Employee referral | 150 | 30 | 27 | 6 |
| Job portal | 2,400 | 60 | 39 | 12 |
| Agency | 400 | 40 | 28 | 24 |
**Asked at:** commonly asked (no company-specific report found); source-effectiveness is a standard recruitment-analytics theme in prep-site question banks (unverified).
**What the interviewer is checking:** Whether you judge a source on cost AND quality (retention), not on volume alone.
**Say this in the interview:** "I would compare cost per hire, hire rate and 12-month retention together. On this data referrals win: cheapest per retained hire and best retention; the agency is the most expensive."
**Clarify first:** Are the three sources hiring for similar roles and levels? Is 12-month retention measured for the same joining period? Any capacity limit on referrals? I will assume like-for-like roles.
**Structure:** Efficiency (applicant-to-hire), cost (per hire, per retained hire), quality (retention), scalability (volume available).
**What I would check, in order:** Compute the four ratios below; then split by role family and seniority; then check time-to-fill by source (not given).
**Numeric work (if data given):**

| Source | Hire rate (hires/applicants) | 12-mo retention | Cost per hire | Cost per retained hire |
|---|---|---|---|---|
| Referral | 20.0% | 90.0% | INR 0.20 lakh | INR 0.22 lakh |
| Job portal | 2.5% | 65.0% | INR 0.20 lakh | INR 0.31 lakh |
| Agency | 10.0% | 70.0% | INR 0.60 lakh | INR 0.86 lakh |

Hire rate = hires / applicants; retention = still employed / hires; cost per retained hire = total cost / still employed (6/27, 12/39, 24/28). Portal and referral have the same cost per hire, but 21 of the portal's 60 hires left against 3 of 30 referral hires, so the portal costs about 38% more per hire that stays.
**If the data shows...:** If referral hires are all junior and the portal supplies the senior roles, the comparison is not like-for-like; compare within role. If referrals are a small pool (150 applicants), more investment means a higher bonus, and cost per hire will rise; test with a pilot.
**Recommendation:** Invest more in referrals (bigger bonus, easier process), keep the portal for volume, and cut agency use to hard-to-fill roles. Track cost per retained hire quarterly. Watch diversity: referrals can copy the existing workforce.
**Likely follow-ups:** 1) *Referral pool is limited, what then?* Use the portal for volume and improve its screening. 2) *Why not just cost per hire?* It hides the portal's weak retention.
**Common mistakes / traps:** Picking the source with most hires; ignoring retention; forgetting referral bonuses are part of the cost.

### Q21 ⭐⭐⭐ 🟡 Teams with low engagement-survey scores also show higher attrition. Can you say low engagement causes attrition, and what would you do next?
Inline data: 40 teams; correlation between team engagement score and next-12-month attrition is -0.45.
**Asked at:** commonly asked (no company-specific report found); root-cause use of engagement data is a recurring people-analytics theme on prep sites (unverified).
**What the interviewer is checking:** Correlation versus causation, and a practical next step.
**Say this in the interview:** "No, not on this alone. A correlation of -0.45 across 40 teams says they move together; it does not say which drives which, or whether a third factor drives both."
**Clarify first:** When was the survey taken relative to exits? Is it anonymous, and at team level? Are small teams noisy? How is attrition defined?
**Structure:** Possible explanations: (1) engagement causes exits; (2) reverse: exits or layoffs lower the morale of those who stay; (3) a common cause (a bad manager, workload, pay freeze, a location); (4) chance or small-team noise.
**What I would check, in order:** Timing: survey before exits (the question uses next-12-month attrition, which helps, but check). Which questions drive the link (manager, growth, pay). Compare within the same grade, location and manager level. Plot the 40 points; one outlier team can create a correlation.
**If the data shows...:** If the link stays after controlling for location and role and the survey precedes the exits, engagement is a credible early-warning signal. If it vanishes within the same manager group, manager quality is the real driver.
**Numeric work (if data given):** r = -0.45, so r squared = 0.2025: about 20% of the variation in team attrition is linearly associated with engagement; about 80% is not.
**Recommendation:** Call it an early-warning indicator, not a proven cause. Run an action pilot: improve engagement in some low-score teams, keep similar teams as comparison, and measure attrition after 12 months.
**Likely follow-ups:** 1) *How to prove cause?* Pilot with a comparison group, or an experiment-like rollout. 2) *Is -0.45 strong?* Moderate.
**Common mistakes / traps:** Saying "engagement causes attrition"; treating r as a percentage; ignoring that leavers never answer next year's survey.

### Q22 ⭐⭐⭐ 🟡 A 250-person plant works 22 days a month and recorded 440 absent person-days last month. What is the absenteeism rate, and what cuts would you apply to understand it?
Inline data: employees 250; working days 22; absent person-days 440.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct denominator (scheduled person-days) and sensible cuts.
**Say this in the interview:** "Absenteeism rate is absent days divided by scheduled days: 440 over 5,500 is 8%. Then I would cut it by day of week, shift, department, tenure and leave type."
**Definition in plain words:** Share of scheduled working days lost to unplanned absence. Rate = absent person-days / (employees x working days) x 100.
**Worked answer:** Scheduled person-days = 250 x 22 = 5,500. Rate = 440 / 5,500 = 0.08 = 8.0%. Per employee: 440 / 250 = 1.76 absent days a month, or 440 / 22 = 20 people absent on an average day.
**Result:** 8% absenteeism (about 20 people absent daily).
**Check:** 8% of 5,500 = 440. Edge case: if some people joined mid-month, use actual scheduled days instead of 250 x 22.
**What I would check, in order:** Day of week (Monday and Friday spikes), shift and department, tenure, age band, supervisor, month and festival or payday timing, and leave type (sick, casual, unauthorised). Then separate a few long absences from many short ones: 10 people absent 20 days each is a different problem from everyone missing 2 days.
**Caveats:** Decide whether approved leave counts; many firms count only unplanned absence. Add a trend over months before reacting. Frequent short absences hint at engagement or supervisor issues; long ones hint at health.
**Likely follow-ups:** 1) *Is 8% high?* Compare with your own history and industry peers; I would not quote a benchmark without a source. 2) *What action?* Target the cut with the highest concentration.
**Common mistakes / traps:** Dividing by 250 only (ignoring days); counting weekly offs in the denominator; reading one month as a trend.

### Q23 ⭐⭐⭐ 🟡 A selection process shortlisted 50 of 200 male applicants and 18 of 120 female applicants. Apply the four-fifths rule and explain what it tells you and what it does not.
Inline data: men 50 of 200; women 18 of 120.
**Asked at:** commonly asked (no company-specific report found); stage-wise adverse-impact monitoring appears in vendor and prep content (unverified).
**What the interviewer is checking:** You can compute the impact ratio and know it is a screening flag, not a verdict.
**Say this in the interview:** "Men are shortlisted at 25% and women at 15%. The ratio is 0.60, below the 0.80 line, so this is a red flag worth investigating, not proof of discrimination."
**Definition in plain words:** The four-fifths (80%) rule compares each group's selection rate with the highest group's rate. Impact ratio = lower rate / higher rate; below 0.80 flags possible adverse impact.
**Worked answer:** Men: 50/200 = 25%. Women: 18/120 = 15%. Impact ratio = 15 / 25 = 0.60. To reach 0.80, women would need a 20% rate: 24 of 120, so 6 more women (18 vs 24). A two-proportion z-test gives z about 2.12, p about 0.034, so the gap is unlikely to be pure chance at the usual 5% level.
**Result:** Impact ratio 0.60, below 0.80: flagged.
**Check:** 0.8 x 25% = 20%; 20% of 120 = 24. Rule uses selection rates, not counts.
**Caveats:** It is a rule of thumb from US practice; it ignores sample size (small groups can fail by chance), job-relevant criteria (experience, qualifications) and applicant mix. It does not show intent or cause. Next: look within role, qualification and source, and see which screening step (resume filter, test) created the gap.
**Likely follow-ups:** 1) *What if the ratio were 0.85?* Passes the rule of thumb, still monitor. 2) *What do you do now?* Review the criteria, check job-relatedness, involve legal or HR.
**Common mistakes / traps:** Comparing counts (50 vs 18) instead of rates; calling it proof of bias; ignoring significance and role mix.

### Q24 ⭐⭐⭐ 🟡 A team needs 240 hires this year. The funnel converts 5% of sourced candidates to screen-pass, 25% of screen-pass to interview-pass, 40% of interview-pass to offer and 75% of offers to joiners. How many candidates must be sourced, and how many recruiters are needed if one recruiter can source 1,200 a year?
Inline data: sourced to screen-pass 5%; screen-pass to interview-pass 25%; interview-pass to offer 40%; offer to join 75%; hires needed 240; recruiter capacity 1,200 sourced per year.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Working a funnel backwards and turning it into capacity.
**Say this in the interview:** "Work backwards from 240 joiners by dividing by each conversion. That needs 64,000 sourced candidates, so about 54 recruiters at 1,200 each."
**Definition in plain words:** Required volume at a stage = volume needed at the next stage / conversion rate of this step.
**Worked answer:**
1. Offers needed = 240 / 0.75 = 320.
2. Interview-pass needed = 320 / 0.40 = 800.
3. Screen-pass needed = 800 / 0.25 = 3,200.
4. Sourced = 3,200 / 0.05 = 64,000.
5. Recruiters = 64,000 / 1,200 = 53.3, round up to 54.
**Result:** 64,000 sourced; 54 recruiters.
**Check:** Forward: 64,000 x 0.05 x 0.25 x 0.40 x 0.75 = 240. Overall conversion = 0.375%, about 267 sourced per hire.
**Caveats:** Real funnels vary by role; add a buffer for offer-to-join drop-outs and seasonal peaks. Capacity of 1,200 ignores screening and interview effort, which also needs people. If the screen-pass rate improved to 6%, sourcing would fall to about 53,333; the first step moves the answer most.
**Likely follow-ups:** 1) *Why round up?* You cannot hire 0.3 of a recruiter. 2) *How to cut the load?* Improve the top-of-funnel quality (better targeting, referrals).
**Common mistakes / traps:** Multiplying instead of dividing; stopping at offers; rounding recruiters down.

### Q25 ⭐⭐ 🟢 What is the difference between headcount and FTE, and how do you compute FTE for 30 full-time employees and 10 part-timers working 20 hours a week against a 40-hour full-time week?
Inline data: full-time employees 30; part-timers 10 at 20 hours per week; full-time week 40 hours.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know headcount counts people and FTE counts workload.
**Say this in the interview:** "Headcount is 40 people; FTE is 35, because ten half-time staff equal five full-time workers."
**Definition in plain words:** Headcount = number of people on the payroll. FTE (full-time equivalent) = total hours worked / hours of one full-time employee.
**Worked answer:** Full-time FTE = 30 x 1.0 = 30. Part-time FTE each = 20 / 40 = 0.5, so 10 x 0.5 = 5. Total FTE = 30 + 5 = 35. Headcount = 30 + 10 = 40.
**Result:** Headcount 40; FTE 35.
**Check:** Hours: (30 x 40) + (10 x 20) = 1,400 hours; 1,400 / 40 = 35.
**Caveats:** Use FTE for capacity and cost planning (cost per FTE), headcount for benefits, licences and people counts. Attrition per headcount and per FTE can differ. Define the full-time week (40 or 45 hours) once in the metrics dictionary.
**Likely follow-ups:** 1) *Do contractors count?* Decide and document; often counted in FTE but not in employee headcount. 2) *Which for productivity?* FTE.
**Common mistakes / traps:** Reporting 40 as FTE; counting each part-timer as 1; mixing definitions across reports.

### Q26 ⭐⭐ 🟢 How does staff turnover differ from attrition, and does the difference matter for reporting?
**Asked at:** commonly asked (no company-specific report found); the two terms are used loosely in prep material (unverified).
**What the interviewer is checking:** That you know the terms are often confused and insist on a written definition.
**Say this in the interview:** "Definitions vary by company. Commonly, turnover counts every exit and replacement flow, while attrition counts leavers who are not replaced or only certain exits. So I would confirm the definition before comparing numbers."
**Explain simply:**
- **Turnover** (common usage): all employees leaving (resignations, dismissals, retirements, end of contract) as a share of average headcount, sometimes including the new hires who replace them.
- **Attrition** (common usage): exits as a natural shrinkage, sometimes only voluntary exits, sometimes counting positions that are not refilled. Some firms use the two words as the same thing.
- Worked mini-example: average headcount 1,000; 150 exits (100 resignations, 30 retirements and terminations, 20 contract ends). All exits: 15%. Resignations only: 10%. Both could be called "attrition" by different teams.
- It matters: leadership may compare 10% with a 15% benchmark and draw the wrong conclusion. Also decide whether internal transfers and contract ends count as exits.
**Practice step:** Write your company's one-line definition of attrition (numerator, denominator, period) and share it with every report.
**Likely follow-ups:** 1) *Which do you report?* Both: total exits and voluntary exits, labelled. 2) *Denominator?* Average headcount for the period.
**Common mistakes / traps:** Comparing numbers built on different definitions; assuming a textbook meaning is universal.

### Q27 ⭐⭐ 🟢 In a survey of 100 employees, 60 are promoters, 25 are passives and 15 are detractors on the 0-10 recommend question. What is the employee Net Promoter Score (eNPS)?
Inline data: promoters 60; passives 25; detractors 15.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct formula and sensible reading.
**Say this in the interview:** "eNPS is percent promoters minus percent detractors: 60% minus 15% is +45."
**Definition in plain words:** Employees are asked "how likely are you to recommend this company as a place to work?" (0-10). Promoters score 9-10, passives 7-8, detractors 0-6. eNPS = %promoters - %detractors, on a scale of -100 to +100.
**Worked answer:** Promoters 60/100 = 60%; detractors 15/100 = 15%; passives (25%) are ignored. eNPS = 60 - 15 = +45.
**Result:** +45 (a number, not a percentage).
**Check:** 60 + 25 + 15 = 100. Range check: all promoters gives +100, all detractors gives -100.
**Caveats:** Judge it against your own past scores and across teams, not against outside "good" scores. Check response rate and anonymity; a small team of 10 swings wildly. Passives still matter: a team with 0 promoters and 0 detractors scores 0 but is lukewarm.
**Likely follow-ups:** 1) *Is +45 good?* It is positive and well above zero; trend and comparison decide. 2) *Why ignore passives?* They are neutral by design.
**Common mistakes / traps:** Writing 45%; including passives; comparing small teams on tiny differences.

### Q28 ⭐⭐ 🟢 What is billable utilisation in a services company, and what is it for a consultant with 1,320 billable hours out of 1,800 available hours?
Inline data: billable hours 1,320; available hours 1,800.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Definition, denominator choice and what the number implies for pricing and staffing.
**Say this in the interview:** "Utilisation is billable hours divided by available hours: 1,320 over 1,800 is 73.3%."
**Definition in plain words:** The share of a person's available time that is charged to clients. Utilisation = billable hours / available hours x 100.
**Worked answer:** 1,320 / 1,800 = 0.7333, so 73.3%. Non-billable time = 480 hours (26.7%): training, bench time, internal work, pre-sales.
**Result:** 73.3%.
**Check:** 73.3% of 1,800 = 1,320.
**Caveats:** "Available" must be defined: net of leave and holidays or gross? Different denominators give different rates. Higher is not always better: very high utilisation leaves no time to train or rest and may raise attrition. Targets vary by grade (juniors usually higher), so compare within grade. For HR, utilisation links to hiring plans, bench cost and burnout.
**Likely follow-ups:** 1) *Target?* Set by the firm and level; I would not quote one without data. 2) *Link to attrition?* Very high or very low utilisation can both push exits.
**Common mistakes / traps:** Using 2,080 total hours instead of available hours; calling bench time billable; pushing utilisation to 100%.

### Q29 ⭐⭐ 🟢 What is a yield ratio in recruiting, and what is the yield from interview to offer if 120 interviews produced 30 offers?
Inline data: interviews 120; offers 30.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can define stage conversion and read it.
**Say this in the interview:** "A yield ratio is the percentage of candidates who pass from one stage to the next. Here 30 offers from 120 interviews is 25%, or one offer per four interviews."
**Definition in plain words:** Yield = candidates who move to the next stage / candidates who entered this stage x 100.
**Worked answer:** 30 / 120 = 0.25 = 25%. Equivalent: 120 / 30 = 4 interviews per offer.
**Result:** 25% interview-to-offer yield.
**Check:** 25% of 120 = 30.
**Caveats:** Define whether the base is candidates interviewed or interview rounds; a candidate with three rounds is counted once. Compare yield by role and interviewer; a very high yield suggests the earlier screen is strong, a very low one suggests it is weak or the bar is unclear. Use yield to plan: for 10 offers you need about 40 interviews.
**Likely follow-ups:** 1) *Is 25% good?* Compare with your own history by role. 2) *Overall yield?* Multiply stage yields.
**Common mistakes / traps:** Counting interview rounds instead of candidates; comparing yields from different roles.

### Q30 ⭐⭐ 🟢 How do you protect employee privacy when sharing attrition or pay analysis, and when do you suppress small groups?
**Asked at:** commonly asked (no company-specific report found); data confidentiality is a named theme in people-analytics question banks (unverified, startup.jobs snippet).
**What the interviewer is checking:** That you treat employee data as sensitive and know practical safeguards.
**Say this in the interview:** "I share only the detail needed, use aggregates, hide groups that are too small to be anonymous, and limit who can see the raw file."
**Explain simply:**
- **Minimise:** drop names, employee IDs, exact dates of birth and other identifiers; share groups, not individuals.
- **Suppress small cells:** a cut with, say, fewer than 5 to 10 people (a threshold your policy sets) is hidden or merged, because anyone could guess who it is. Example: "attrition in the Pune finance team: 1 of 4" is effectively naming a person.
- **Watch the subtraction trap:** if the total and every other group are shown, a hidden cell can be worked out. Hide a second cell or combine groups.
- **Round or band:** show pay in bands, ages in ranges.
- **Control access:** role-based access, password-protected files, no personal email, share dashboards rather than extracts.
- **Follow the rules and purpose:** use data only for the stated purpose, in line with company policy and the applicable law (India's data protection rules); check with legal.
**Mini-example:** A 3-woman engineering team's average pay shown by gender reveals each woman's pay range. Combine with neighbouring teams instead.
**Likely follow-ups:** 1) *What threshold?* Set by policy; common practice is a minimum group of a handful of people. 2) *Exit-interview comments?* Anonymise or summarise themes.
**Common mistakes / traps:** Emailing raw files; reporting tiny cells; forgetting that combining filters can re-identify people.

### Q31 ⭐⭐ 🟢 Why do offer-to-joining drop-outs ('renege' rate) matter more in India than in many markets, and how would you measure them?
**Asked at:** commonly asked (no company-specific report found); the reasoning below is judgement, not a verified statistic.
**What the interviewer is checking:** Context awareness of the Indian hiring market and a clear metric.
**Say this in the interview:** "The gap between offer and joining can be long, and candidates often hold several offers, so a share of accepted offers never turns into joiners. I measure it as joiners over accepted offers and cut it by notice period and source."
**Explain simply:**
- Why it can matter more (reasoning, unverified): notice periods in India are often long (commonly one to three months for lateral hires), campus offers can wait many months before joining, and candidates can hold several offers or receive counter-offers from their current employer. A long wait is more time for something to change.
- A drop-out wastes sourcing and interview cost, delays projects, and forces restarts.
- **Measure:** Renege rate = (offers accepted but not joined) / offers accepted x 100. Also track offer-to-join conversion = joiners / offers extended.
- Worked mini-example: 100 offers, 80 accepted, 68 joined. Offer acceptance = 80%; renege rate = 12 / 80 = 15%; offer-to-join = 68%.
- **Cuts:** notice-period length, source, role, salary hike offered, candidate's current company, recruiter and time-to-offer, and the contact frequency during the notice period.
- **Levers to test:** regular engagement during notice period, early joining bonus, faster offer-to-onboard process, backup candidates.
**Practice step:** Compute the renege rate by notice-period band from last year's offers.
**Likely follow-ups:** 1) *How to cut it?* Test engagement and joining bonuses on random groups. 2) *Different from acceptance rate?* Acceptance is at the offer stage; renege is after acceptance.
**Common mistakes / traps:** Using offers extended instead of accepted as the base without labelling; counting only joiners.

### Q32 ⭐⭐ 🟡 The marketing department's attrition fell from 20% to 18% and the engineering department's fell from 12% to 10%, yet company-wide attrition rose. Is that possible, and how would you show it from the data below?
| Department | Year 1 headcount | Year 1 leavers | Year 2 headcount | Year 2 leavers |
|---|---|---|---|---|
| Marketing | 500 | 100 | 800 | 144 |
| Engineering | 500 | 60 | 200 | 20 |

(Check: compute each department's and the combined rate for both years.)
**Asked at:** commonly asked (no company-specific report found); Simpson-type composition pitfalls are a gap-fill topic of this book (judgement).
**What the interviewer is checking:** Recognising a mix (composition) effect, a Simpson-type paradox.
**Say this in the interview:** "Yes. Each department improved, but headcount shifted towards marketing, the department with the higher attrition, so the blended rate rose from 16.0% to 16.4%."
**Definition in plain words:** Company attrition is a weighted average of department rates, weighted by headcount. Changing the weights can raise the total even if every part improves. (Here I use year headcount as the denominator, as the table gives it.)
**Worked answer:** Marketing: 100/500 = 20.0% in year 1; 144/800 = 18.0% in year 2. Engineering: 60/500 = 12.0%; 20/200 = 10.0%. Combined year 1: 160/1,000 = 16.0%. Year 2: 164/1,000 = 16.4%. Weights: marketing 50% to 80%, engineering 50% to 20%.
**Result:** Both departments improved by 2 points; company rose from 16.0% to 16.4%.
**Check:** Hold year 1 weights fixed (50/50) with year 2 rates: 0.5 x 18% + 0.5 x 10% = 14.0%, so like-for-like attrition fell 2 points; the mix shift added back 2.4 points (14.0% to 16.4%).
**Caveats:** Neither headline is wrong; it answers different questions. Report department rates with the mix, or a mix-adjusted (standardised) rate. Check why the mix changed: was engineering shrinking through layoffs, transfers or growth in marketing?
**Likely follow-ups:** 1) *Which number goes to the board?* Both, with the mix explained. 2) *Name of this effect?* Simpson-type or composition effect.
**Common mistakes / traps:** Calling the data wrong; averaging the two department rates without weights.

### Q33 ⭐⭐ 🟡 How would you build a model to predict which employees will resign in the next six months? Cover the target, features, leakage, evaluation and how HR should use the output.
**Asked at:** commonly asked (no company-specific report found); predicting turnover is a named theme in people-analytics interview banks (startup.jobs, unverified).
**What the interviewer is checking:** A full modelling workflow with sensible HR judgement, including ethics.
**Say this in the interview:** "I would define the target carefully, build features that were known at the prediction date, avoid leakage, evaluate on a later time period, and use the scores to prioritise conversations, not to judge people."
**Clarify first:** What is the use (retention conversations)? Voluntary exits only? Who is in scope? How much history is there (at least two years)?
**Structure:**
- **Target:** snapshot each employee on a date (monthly); label 1 if they resign voluntarily within the next six months, else 0. Exclude layoffs and retirements, or model them separately.
- **Features (known at snapshot date):** tenure, grade, time since last promotion or raise, compa-ratio, manager and span, recent rating, engagement score, leave and absence pattern, commute or location, team attrition, market conditions.
- **Leakage:** anything created after the decision: notice-period flags, exit-interview data, "handover started", a post-resignation rating change. Also a random split that lets the same person appear in train and test.
- **Evaluation:** train on earlier snapshots, test on later ones; check precision, recall and lift at the top 10% of scores, not accuracy (leavers are a minority). Check calibration.
- **Fairness:** compare error rates across gender, age, and so on; avoid using protected traits and proxies.
**What I would check, in order:** Baseline (a simple rule such as short tenure and no raise); logistic regression first, then gradient boosting; compare lift.
**Recommendation:** HR uses scores to rank who gets a stay conversation; managers see themes, not scores; track whether the interventions reduce attrition against a comparison group. Do not use scores for performance or promotion decisions.
**Likely follow-ups:** 1) *Why not accuracy?* With 10% leavers, "nobody leaves" is 90% accurate. 2) *Explainability?* Share main drivers per group, not individual predictions.
**Common mistakes / traps:** Leakage; random split; reporting accuracy; acting on scores without a plan or privacy care.

### Q34 ⭐⭐ 🟡 An attrition model flags 200 of 2,000 employees as high risk. Over the next six months 150 employees actually leave, of whom 60 were in the flagged group. Compute precision and recall, and say whether the model is useful.
Inline data: employees 2,000; flagged 200; actual leavers 150; leavers among flagged 60.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct precision and recall, and judgement on usefulness against the base rate.
**Say this in the interview:** "Precision is 30% and recall is 40%. The base rate is only 7.5%, so the flagged group is four times as likely to leave as a random employee: useful for prioritising, but it still misses 60% of leavers."
**Definition in plain words:** Precision = of those flagged, the share who left = true positives / flagged. Recall = of those who left, the share we flagged = true positives / actual leavers.
**Worked answer:** Precision = 60 / 200 = 30%. Recall = 60 / 150 = 40%. Base rate = 150 / 2,000 = 7.5%. Lift = 30% / 7.5% = 4.0. Flagged non-leavers = 140; unflagged leavers = 90 out of 1,800 unflagged (5.0%).
**Result:** Precision 30%, recall 40%, lift 4x.
**Check:** 60 + 90 = 150 leavers; 60 + 140 = 200 flagged.
**Caveats:** Usefulness depends on the cost of action: if a stay conversation is cheap, 70% false alarms is tolerable; if each action is a costly bonus, it is not. Compare with a simple rule (tenure under 2 years) to see if the model adds anything. Some leavers (relocation, health) are unpredictable, so recall will never be near 100%. Also check fairness across groups.
**Likely follow-ups:** 1) *Increase recall?* Flag more people; precision usually falls. 2) *F1?* Combines both: 2 x 0.3 x 0.4 / 0.7 = 0.343.
**Common mistakes / traps:** Swapping precision and recall; ignoring the base rate; judging by accuracy (1,850 of 2,000 correct sounds great, but it is mostly non-leavers).

### Q35 ⭐⭐ 🟡 First-year attrition of campus hires is 30% against 10% for lateral hires. How do you diagnose this?
Inline data available: campus-hire records (college tier, branch, offer date, joining date, training batch, project allocation, manager, first-year rating) and exit reasons.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Structured diagnosis using the data listed, and awareness of comparison pitfalls.
**Say this in the interview:** "I would first check the comparison is fair, then locate when and where campus hires leave, and test whether the cause is selection, onboarding or role mismatch."
**Clarify first:** Same definition of first year for both groups (campus hires count from joining, not offer)? Do exits include those who left in training? Which roles, locations, years?
**Structure:** (1) Selection: wrong colleges, branches or expectations. (2) Onboarding and training: poor batches, long bench time. (3) Role and project fit: allocation different from the promise. (4) Manager and team. (5) Market pull and pay: other offers, pay gap versus the market. (6) Comparison issue: campus hires are younger and more mobile; laterals already survived a job search.
**What I would check, in order:** Exit timing (month of leaving: spike at 3, 6 or 12 months); attrition by college tier and branch; by training batch and bench time before allocation; by project type and manager; by first-year rating; exit reasons grouped; pay versus laterals in the same grade.
**If the data shows...:** Early exits concentrated in some batches or on long bench waits: onboarding and allocation fix. Concentrated in a college tier or branch: change campus mix or the offer pitch. Spread across all, with pay or growth reasons: compensation and career path. Exits mostly low-rated hires: partly healthy attrition; high-rated leavers are the concern.
**Recommendation:** Fix the biggest concentration first, such as bench time under a set number of days, buddy programmes and early manager check-ins at 30, 60, 90 days. Track the 12-month retention of new cohorts against the old.
**Likely follow-ups:** 1) *Is 30% simply normal for freshers?* Unknown without an internal history; trend by cohort. 2) *Is some attrition fine?* Yes if low performers leave.
**Common mistakes / traps:** Comparing campus to laterals as if identical; ignoring exit timing; mixing regretted and non-regretted exits.

### Q36 ⭐⭐ 🟡 One manager's team of 20 lost 8 people in a year while the company average is 12%. How do you decide whether this manager is a problem?
Inline data: team size 20; leavers 8; company-wide attrition 12%.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Small-sample judgement: not jumping to blame, but not dismissing a real signal.
**Say this in the interview:** "The team lost 40% against 12%, about 2.4 expected leavers versus 8 actual. That is very unlikely by chance, but I would check the team's mix and the exit reasons before judging the manager."
**Clarify first:** Is the 12% for comparable roles and locations? Did the team have a layoff, transfer or restructure? Were exits all voluntary? Is the 8 over a stable team of 20?
**Structure:** (1) Is it statistical noise? (2) Is it a mix effect (role, location, tenure)? (3) Is it a manager effect (exit reasons, engagement, history across teams)? (4) Is it a one-off (a project ended, a local competitor hiring)?
**What I would check, in order:** Compare with similar teams, not the whole company; the manager's record in previous teams and whether their old team attrition stays high; exit-interview themes and the engagement score for the manager questions; who left (high performers or low); timing (clustered or spread).
**Numeric work (if data given):** Rate = 8/20 = 40%. Expected at 12% = 2.4. If each person left independently with probability 12%, the chance of 8 or more leaving out of 20 is about 0.14%, so it is unlikely to be chance. Caveat: with many managers, a few will look extreme by chance; one test among 200 managers is a screening flag, not a verdict.
**If the data shows...:** Exit reasons point to the manager and the pattern repeats across his or her teams: coaching, a performance plan or a move. Exits look tied to a specific project or role: fix the workload or pay, not the manager.
**Recommendation:** Do not act on the number alone: hold stay conversations with remaining members, review exit data, and set a 6-month check. Decide with the HR business partner.
**Likely follow-ups:** 1) *Why not blame at once?* Because the cause may sit in role or location. 2) *Why is 20 people a problem?* Small base, so one exit moves the rate by 5 points.
**Common mistakes / traps:** Comparing to company average without context; ignoring noise; treating the test as proof.

### Q37 ⭐⭐ 🟡 A 52-person company with 12 women and 40 men wants a pay equity check. How do you proceed when sample sizes are small?
**Asked at:** commonly asked (no company-specific report found); small-sample aggregation and log-salary regression appear in vendor and institutional pay-equity blogs (unverified).
**What the interviewer is checking:** Realism about what statistics can show with 52 people and a practical approach.
**Say this in the interview:** "With 12 women, a regression has little power, so I would do a role-by-role comparison first, a simple adjusted model with few controls, and then review individual outliers, and I would be honest that a non-significant result is not proof of equity."
**Clarify first:** Is there a job and level structure? Pay components (base, bonus)? Dates of joining, prior experience? Why do we check (legal compliance, trust)?
**Structure:** Descriptive first, then a small model, then case review.
**What I would check, in order:**
1. Unadjusted gap: average and median pay for men and women.
2. Group by job family and level: compare within groups with at least two people from each gender; do not run tests on groups of 1 or 2.
3. Simple regression of log pay on a female indicator plus two or three controls (level, tenure, role); too many controls on 52 people give unstable results. The coefficient on the female indicator is roughly the percent gap.
4. Look at confidence intervals (wide), not only p-values.
5. Review individuals: each woman's pay against peers in the same role and level, and the compa-ratio (pay over band midpoint).
**If the data shows...:** A gap of a few percent with a wide interval including zero: cannot conclude either way; review individual cases and fix clear anomalies. A large consistent gap across several roles: act even if not significant.
**Recommendation:** Combine statistics with case-by-case review, repeat annually, document the rules for pay setting, and suppress group results where the group is below the privacy threshold.
**Likely follow-ups:** 1) *Why not a t-test?* It ignores job and level differences. 2) *Can you pool years?* Yes, with year controls, to add power.
**Common mistakes / traps:** Over-controlling with 52 rows; reading non-significance as fairness; reporting groups of 1 or 2.

### Q38 ⭐⭐ 🟡 Promotion data by gender is below. Compute the promotion rates, and explain how you would test whether the difference is meaningful and what else to check.
| Group | Eligible employees | Promoted |
|---|---|---|
| Men | 400 | 60 |
| Women | 200 | 20 |
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Rates, an appropriate significance test, and awareness of confounders.
**Say this in the interview:** "Men are promoted at 15% and women at 10%, a ratio of 0.67. A two-proportion test gives p of about 0.09, so it is suggestive but not conclusive at 5%; I would check role, grade and time in grade before concluding."
**Definition in plain words:** Promotion rate = promoted / eligible. A significance test asks how likely a gap this big is if the true rates were equal.
**Worked answer:** Men: 60/400 = 15.0%. Women: 20/200 = 10.0%. Difference = 5 percentage points; ratio 10 / 15 = 0.67. Pooled rate = 80/600 = 13.3%. Two-proportion z-test: z about 1.70, p about 0.09 (two-sided). Fisher's exact test (better for smaller counts) gives p about 0.10.
**Result:** 15% versus 10%; p about 0.09 to 0.10, not significant at the 5% level but borderline.
**Check:** Equal rates would give 26.7 women promoted (13.3% of 200) against 20 observed, a shortfall of about 6.7 promotions.
**Caveats:** Non-significant does not mean no difference: with these counts the test has limited power. Check: who counts as eligible; grade, function, location, time since last promotion and performance rating (compare within these groups, not overall, and watch for the Simpson-type mix problem); manager variation; whether women were promoted at lower rates in specific functions; trend over several years (pool years for power). If the rating itself is biased, controlling for it can hide the issue.
**Likely follow-ups:** 1) *What if p were 0.01?* A gap this big would be unlikely by chance, still not proof of the cause. 2) *Effect size?* Report the 5-point gap and ratio with a confidence interval.
**Common mistakes / traps:** Treating p of 0.09 as "no difference"; comparing counts (60 vs 20); ignoring grade and eligibility definitions.

### Q39 ⭐⭐ 🟡 The company has a payroll of INR 50 crore and an 8% increment budget. How much is the budget, and how would you design the allocation across performance ratings and compa-ratios?
Inline data: payroll INR 50 crore; increment budget 8%.
**Asked at:** commonly asked (no company-specific report found); compensation-planning cases appear in HR-analytics question banks (unverified prep-site material).
**What the interviewer is checking:** Whether you size the pool first, then allocate it by a rule (performance and position in pay range) that adds back to the budget.
**Say this in the interview:** "The pool is 8% of 50 crore, so INR 4 crore. I would split it with a merit matrix: higher rating gets a bigger increment, and within a rating, people paid low for their grade get a bit more than those already at the top of the range. Then I check the matrix adds up to 4 crore."
**Clarify first:** Is the 8% of fixed pay for all staff or eligible staff only? Do promotions and market corrections come inside this 8% or on top? Is there a budget cap per person? I will assume it is everything, in one pool.
**Structure:**
- Pool = 8% x INR 50 crore = INR 4 crore.
- Compa-ratio (plain words: an employee's pay divided by the midpoint of their grade's pay range; 1.00 means paid exactly at midpoint). Below 0.90 is low in range, above 1.10 is high.
- Matrix: base increment by rating, plus or minus a compa-ratio adjustment.
**What I would check, in order:** (1) Payroll split by rating (assumed, unverified): rating 5 = 10%, 4 = 25%, 3 = 50%, 2 = 12%, 1 = 3%. (2) Compa-ratio bands within each rating (assumed): low 25%, mid 55%, high 20% of payroll. (3) In Excel, SUMPRODUCT of payroll x increment % per cell, compared with 4 crore.
**If the data shows...:** Many people high in range means the matrix saves money and I can fund more for the low-range top performers. Many low-range people means the matrix overspends, so I trim increments on rating 3 first, not on rating 5.
**Numeric work (if data given):** Base increments: 5 = 14%, 4 = 10.5%, 3 = 7%, 2 = 3%, 1 = 0%. Weighted base = 0.10x14 + 0.25x10.5 + 0.50x7 + 0.12x3 + 0 = 7.885%. Compa adjustment: +1.5 points for low band, 0 mid, -1.5 high; weighted = 0.25x1.5 - 0.20x1.5 = +0.075 points. Total = 7.96%, which is INR 3.98 crore, leaving about INR 2 lakh unspent as buffer.
**Recommendation:** Publish the matrix, run it on actual payroll before announcing, and measure afterwards: do top performers leave less than before, and is the pay gap by rating widening as intended?
**Likely follow-ups:** 1) *Why not equal 8% for all?* It rewards nobody in particular and top performers may leave. 2) *What if the matrix overshoots?* Scale every cell by 4.00/4.20 instead of cutting one group.
**Common mistakes / traps:** Forgetting to check the matrix adds up to the pool; ignoring compa-ratio so low-paid people stay low; treating the pool as 8% of CTC when it is 8% of fixed pay (definitions differ).

### Q40 ⭐⭐ 🟡 A company with 1,000 employees expects 18% attrition and wants net headcount growth of 120 this year. How many hires are needed, and what does that imply for the recruiting plan?
Inline data: opening headcount 1,000; attrition 18%; net growth target 120.
**Asked at:** commonly asked (no company-specific report found); workforce-planning arithmetic appears in HR-analytics question banks (unverified).
**What the interviewer is checking:** Whether you replace leavers AND add the growth, and then turn hires into a recruiting funnel.
**Say this in the interview:** "Attrition of 18% on 1,000 is 180 leavers. To end at 1,120 I need 180 plus 120, so about 300 hires, roughly 25 a month, and with offer drop-offs that means around 375 offers."
**Definition in plain words:** Hires needed = leavers to replace + net growth wanted. Leavers = attrition rate x headcount base.
**Worked answer:** 1) Leavers = 18% x 1,000 = 180 (using opening headcount). 2) Hires = 180 + 120 = 300. 3) Monthly = 300 / 12 = 25 hires. 4) Funnel with assumed 80% offer acceptance: offers = 300 / 0.80 = 375. With an assumed 25% offer-per-interview rate, about 1,500 interviews. (Both rates are assumed, unverified.)
**Result:** 300 hires a year, about 25 a month, about 375 offers.
**Check:** If headcount grows to 1,120, average headcount is about 1,060, so 18% gives about 191 leavers and 311 hires. The simple 300 is fine for a first answer; state that it is slightly low.
**Caveats:** Attrition is rarely even through the year, so hiring should be front-loaded to cover seasonal exits. Hiring takes time, so open requisitions 2 to 3 months ahead of need. Part of the 300 can come from internal moves or freshers' campus batches. If attrition is 18% but concentrated in one team, the recruiting plan should be skill-specific, not a flat 25.
**Likely follow-ups:** 1) *What if attrition rises to 22%?* Leavers 220, hires 340. 2) *What does it imply for the recruiting team?* Check recruiter capacity: 375 offers needs roughly 1,500 interviews. 
**Common mistakes / traps:** Hiring only 120 (forgetting replacements); applying 18% to the closing headcount; ignoring offer drop-offs and joining delays.

### Q41 ⭐⭐ 🟡 Replacing a leaver is estimated to cost 50% of annual CTC. If 60 people with an average CTC of INR 12 lakh left, what is the cost of attrition, and how much would a retention programme costing INR 1.2 crore have to save to break even?
Inline data: leavers 60; average CTC INR 12 lakh; replacement cost 50% of CTC; programme cost INR 1.2 crore.
**Asked at:** commonly asked (no company-specific report found); cost-of-attrition cases appear in HR-analytics question banks (unverified).
**What the interviewer is checking:** Clean unit handling (lakh and crore) and the break-even logic.
**Say this in the interview:** "Cost per leaver is 50% of 12 lakh, so 6 lakh. Sixty leavers cost 3.6 crore. A 1.2 crore programme breaks even if it prevents 20 exits, one third of the 60."
**Definition in plain words:** Cost of attrition = leavers x replacement cost per leaver. Break-even = programme cost divided by saving per avoided exit.
**Worked answer:** 1) Replacement cost per leaver = 0.5 x 12 lakh = 6 lakh. 2) Total = 60 x 6 lakh = 360 lakh = INR 3.6 crore. 3) Programme cost = 1.2 crore = 120 lakh. 4) Avoided exits to break even = 120 / 6 = 20. 5) 20 / 60 = 33.3% reduction in leavers.
**Result:** INR 3.6 crore cost of attrition; the programme must save at least INR 1.2 crore, which means preventing 20 of 60 exits.
**Check:** 20 x 6 lakh = 120 lakh = 1.2 crore, matching the programme cost.
**Caveats:** The 50% replacement cost is an assumption; real figures differ by role (agency fees, ramp-up lost output, training). It is also a rough planning number, not a cash figure. Counting only avoided exits ignores that the programme may keep the wrong people (low performers). Savings should be judged against a comparison group, since some of the 60 would have stayed anyway.
**Likely follow-ups:** 1) *What if replacement cost is 30%?* 3.6 lakh each, break-even 33 exits, more than half the group. 2) *Is a 33% fall realistic?* Test by pilot, not assumption.
**Common mistakes / traps:** Mixing lakh and crore (1 crore = 100 lakh); using 12 lakh instead of 6 lakh per leaver; ignoring that the programme cost is spent regardless of results.

### Q42 ⭐⭐ 🟡 Offer rates differ across interviewers for similar candidates, as shown below. How do you find out whether this is interviewer bias or candidate mix?
| Interviewer | Candidates interviewed | Offers recommended |
|---|---|---|
| A | 60 | 24 |
| B | 55 | 9 |
| C | 70 | 21 |
**Asked at:** commonly asked (no company-specific report found); funnel-fairness and interviewer-consistency themes appear in HR-analytics question banks (unverified).
**What the interviewer is checking:** Whether you compare like with like (candidate mix) and test whether the differences exceed chance.
**Say this in the interview:** "B's offer rate is 16% against 40% for A and 30% for C. Before calling it bias, I would compare each interviewer on the same role, level and source, and test if the gap is bigger than chance."
**Clarify first:** Were candidates assigned to interviewers randomly? Same role, level, round and scorecard? What did the other panel members decide?
**Structure:**
- Hypothesis 1: candidate mix differs (B got weaker or harder-role candidates).
- Hypothesis 2: interviewers apply different standards (bias or strictness).
- Hypothesis 3: small numbers, so the gap is noise.
**What I would check, in order:** 1) Rates: A 24/60 = 40%, B 9/55 = 16.4%, C 21/70 = 30%; overall 54/185 = 29.2%. 2) Expected offers at the overall rate: A 17.5, B 16.1, C 20.4. 3) Chi-square test across the three: statistic about 7.8, 2 degrees of freedom, p about 0.02, so unlikely to be pure chance. 4) Stratify (split) by role, level, source and resume score, and recompute. 5) For candidates who met several interviewers, compare each one's score on the same candidate.
**If the data shows...:** The gap vanishes after splitting by role or resume score: it was candidate mix. The gap persists inside every segment: interviewer strictness, so calibrate with shared rubrics and a second-interviewer sample. B is strict on everyone equally but fair: standardise the bar, not accuse them.
**Recommendation:** Do not act on raw rates. Run the stratified comparison, then calibration sessions and structured scorecards; track offer rate per interviewer monthly with the candidate-mix controls.
**Likely follow-ups:** 1) *Why not just average?* Averages hide mix. 2) *Is p = 0.02 proof of bias?* No, only that chance alone is unlikely; mix could explain it.
**Common mistakes / traps:** Ranking interviewers by raw rate; testing with tiny samples; concluding bias without controlling for role.

### Q43 ⭐⭐ 🟡 Women are 45% of applicants but only 25% of final-round candidates and 22% of offers. How do you locate where the drop occurs and decide whether it is a problem?
Inline data: women's share of applicants 45%, of shortlisted 38%, of final-round candidates 25%, of offers 22%; data by stage, role, source and recruiter available.
**Asked at:** commonly asked (no company-specific report found); funnel adverse-impact monitoring by stage appears in vendor and prep content (unverified).
**What the interviewer is checking:** Whether you convert shares into stage-by-stage pass rates and find the leakiest stage.
**Say this in the interview:** "I would compute, at each stage, how women's pass-through compares with men's. Women's share falls most between shortlisted and final round, so I would dig there first, then split by role, source and recruiter."
**Clarify first:** Is 45% the share of all applicants across all roles? Are roles with different gender mixes pooled? What does "shortlisted" mean, resume screen?
**Structure:** Gender share by stage, then pass rate by gender, then segment cuts (role, source, recruiter, location), then process cause (screen criteria, interview panel, offer negotiation).
**What I would check, in order:** Using the shares given, women's pass rate relative to men's (a ratio; 1.0 means equal):
1) Applicant to shortlist: (38/62) / (45/55) = 0.75.
2) Shortlist to final: (25/75) / (38/62) = 0.54.
3) Final to offer: (22/78) / (25/75) = 0.85.
4) End to end: (22/78) / (45/55) = 0.34.
Then check each by role, source and recruiter in SQL/Power BI (GROUP BY stage, gender).
**If the data shows...:** The largest drop (shortlist to final, ratio 0.54) is well below the four-fifths rule of thumb (0.80), so it is a problem worth investigating. If the drop sits in a few roles or one recruiter, it is local; if everywhere, it is systemic (screening criteria). If women apply mostly to roles with low hiring rates, it is mix (Simpson-type effect), not bias.
**Numeric work (if data given):** Ratios above (rounded to 2 decimals). Two stages (0.75, 0.54) fail the 0.80 rule; the offer stage (0.85) passes.
**Recommendation:** Audit the shortlist-to-final stage first: blind screening, structured criteria, panel diversity; track the stage ratios monthly.
**Likely follow-ups:** 1) *Is 0.80 a law?* No, a screening guideline from US practice; use as a flag. 2) *Where does it start?* Applicant stage may also reflect job-ad reach.
**Common mistakes / traps:** Comparing share points (45 to 22) instead of pass rates; ignoring role mix; claiming causation.

### Q44 ⭐⭐ 🟡 The average gap between men's and women's pay is 15% company-wide, but within each job grade the gap is 2%. How can both be true, and what does each tell you?
Inline data: company-wide gap 15%; gap within each grade 2%; men are concentrated in senior grades.
**Asked at:** commonly asked (no company-specific report found); unadjusted versus adjusted pay-gap questions appear in pay-equity prep content (unverified).
**What the interviewer is checking:** Whether you understand composition effects (more men in senior, better-paid grades) and what each gap measures.
**Say this in the interview:** "Both can be true because the 15% is mostly about WHO is in senior grades, while the 2% is about pay for the same grade. The first points to a representation and promotion problem, the second to a small direct pay gap."
**Explain simply:**
- Unadjusted (company-wide) gap: average men's pay versus average women's pay, regardless of job.
- Adjusted (within-grade) gap: compares like with like.
- If men sit in senior, higher-paid grades, the company-wide average is pulled up for men even if each grade pays equally.
**Worked mini-example (illustrative numbers):** Junior grade pays men 10 lakh, women 9.8 lakh; senior pays men 30 lakh, women 29.4 lakh (2% lower in each). Suppose 30% of men but 19% of women are senior. Men's average = 10 + 0.30 x 20 = 16 lakh. Women's = 9.8 + 0.19 x 19.6 = 13.52 lakh. Gap = (16 - 13.52) / 16 = 15.5%, though each grade shows only 2%.
**What each tells you:** The 2% asks "equal pay for equal work?", a fairness and legal question; the 15% asks "equal access to well-paid roles?", a hiring, promotion and retention question.
**Practice step:** Rebuild the example in Excel with grade shares as inputs and watch the gap move.
**Likely follow-ups:** 1) *Is 2% fine?* Still check it is not larger in specific grades or roles. 2) *How to cut the 15%?* Promotion and hiring pipeline, not pay adjustments.
**Common mistakes / traps:** Saying "no gender pay problem because within-grade is 2%"; treating grade as neutral when promotions may be biased (see the pay-equity regression question).

### Q45 ⭐⭐ 🟡 A bank is rolling out a return-to-office policy of three days a week. How would you measure its effect on attrition, productivity and hiring?
**Asked at:** commonly asked (no company-specific report found); policy-impact questions appear in people-analytics question banks (unverified).
**What the interviewer is checking:** Whether you can design a fair before-and-after comparison with a control group and sensible outcome metrics.
**Say this in the interview:** "I would use difference-in-differences: compare the change in attrition, productivity and hiring for teams under the policy against similar teams not yet affected, because a plain before-and-after confuses the policy with everything else that changed."
**Clarify first:** Is the rollout for all branches at once, or staggered? What is the start date? Are some roles exempt (branch staff already on site)? What decision depends on this?
**Structure:** Three outcome families, each with metric, window and comparison.
- Attrition: monthly voluntary attrition, split regretted and non-regretted, and by tenure and city. Exits often lag the announcement by 3 to 6 months.
- Productivity: bank-specific outputs (loan files processed, tickets closed, targets met); avoid hours logged or badge swipes alone.
- Hiring: offer acceptance rate, applications per opening, time-to-fill.
**What I would check, in order:** 1) Pre-policy trend for 6 to 12 months. 2) Control group: exempt roles or later-rollout teams, matched on role, city, tenure. 3) Difference-in-differences: (treated after - treated before) - (control after - control before). 4) Exit-interview themes and engagement scores as supporting evidence.
**If the data shows...:** Attrition rises only among high-performers or women with caregiving duties: policy hurts specific groups. Productivity flat but hiring pool wider elsewhere: the policy is costing talent without a gain.
**Recommendation:** Report effects with ranges, by segment, at 3, 6 and 12 months; propose exceptions or flexible days where harm concentrates.
**Likely follow-ups:** 1) *No control group?* Use interrupted time series on pre-trend, flagged as weaker. 2) *Seasonality?* Compare year-on-year.
**Common mistakes / traps:** Before-and-after only; using attendance as productivity; reading only the first month of exits.

### Q46 ⭐⭐ 🟡 How would you forecast monthly headcount for the next 12 months for a company that hires in batches and has seasonal resignations?
**Asked at:** commonly asked (no company-specific report found); workforce-planning forecasts appear in HR-analytics question banks (unverified).
**What the interviewer is checking:** A roll-forward model: opening + hires - leavers, with seasonality and batch timing built in.
**Say this in the interview:** "I would roll headcount forward month by month: closing = opening + joiners - leavers, with leavers = a base attrition rate times a seasonal index, and joiners entered on the actual batch dates, then show a range."
**Clarify first:** Does the forecast include planned batches (campus or lateral)? Which units (by team or location)? How many years of monthly history exist?
**Approach:** Bottom-up roll-forward by team, using history for the seasonal pattern; sum to the company.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Opening headcount | 1,000 | example |
| Annual attrition | 18% | example |
| Hiring batches | 60 in Feb, May, Aug, Nov | assumed plan |
| Seasonal index (Jan to Dec) | 1.3, 1.2, 0.8, 0.8, 0.9, 1.0, 1.1, 1.0, 1.0, 0.9, 0.9, 1.1 (sum 12) | appraisal-season exits assumed |
**Calculation:** 1) Monthly leavers = headcount x 18% / 12 x index. 2) January: 1,000 x 1.5% x 1.3 = 19.5, closing 980. 3) February: 980 x 1.5% x 1.2 = 17.6 leavers, plus 60 joiners = 1,023. 4) Continue each month the same way.
**Result:** About 185 leavers over the year and closing headcount about 1,056 (low point 980 in January, never above about 1,073 in November after the batch).
**Sanity check:** 18% x about 1,030 average headcount is about 185, matching the total.
**Sensitivity:** Attrition rate moves the answer most: each 2 points of annual attrition shifts year-end headcount by about 20. Run best, base and worst cases; check forecast error (MAPE) on last year's data.
**Likely follow-ups:** 1) *Where do leavers come from by tenure?* Use tenure-specific rates. 2) *Which tool?* Excel roll-forward, then SARIMA only if history is long.
**Common mistakes / traps:** Using a flat attrition rate; hiring all in one month; ignoring joining delay after offers.

### Q47 ⭐⭐ 🔴 Why is a simple annual attrition rate misleading for tenure analysis, and how would survival analysis (Kaplan-Meier) help? Explain censoring in this context.
**Asked at:** commonly asked (no company-specific report found); survival and tenure analysis appear in people-analytics question banks (unverified).
**What the interviewer is checking:** Whether you understand time-to-event data and why people still employed are not "non-leavers".
**Say this in the interview:** "An annual rate ignores how long people stay and who is still at risk. Kaplan-Meier estimates the share still employed at each tenure, and treats current employees as censored, meaning we only know they stayed at least this long."
**Explain simply:**
- An annual attrition rate is one number: leavers over average headcount. It mixes new joiners and ten-year veterans, so it hides that most exits occur in year one.
- Survival analysis asks: of those who joined, what share is still here after 3, 6, 12 months?
- Censoring: employees who have not left yet (or left for a reason you exclude, such as retirement) have an unknown final tenure. We know only that it is at least their current tenure. Dropping them or counting them as "stayers forever" biases results.
- Kaplan-Meier: at each exit time, multiply survival by (1 - leavers / people still at risk).
**Worked mini-example:** 10 employees, tenure in months (L = left, C = still employed): 3L, 5L, 6C, 8L, 10L, 12C, 14L, 18C, 20C, 24C. Survival: month 3: 1 - 1/10 = 0.90; month 5: x (1 - 1/9) = 0.80; month 8 (7 at risk): 0.686; month 10 (6 at risk): 0.571; month 14 (4 at risk): 0.429. Median tenure is about 14 months, where survival drops below 0.5. A naive "5 of 10 left = 50%" ignores time.
**Practice step:** Do this in Python's lifelines or Excel, then compare joiner cohorts or teams with a log-rank test.
**Likely follow-ups:** 1) *Why not a simple average tenure?* Biased low for recent joiners. 2) *Next step?* Cox model for what predicts exit.
**Common mistakes / traps:** Treating censored employees as non-events with full follow-up; mixing cohorts; comparing rates across different tenure mixes.

### Q48 ⭐⭐ 🔴 The company gave retention bonuses to 300 high performers and attrition in that group fell from 15% to 9%. How do you judge whether the bonus worked when it was not randomised?
Inline data: treated group 300 employees, attrition 15% before and 9% after; comparison group of 900 other employees, attrition 12% before and 10% after.
**Asked at:** commonly asked (no company-specific report found); retention-programme evaluation appears in people-analytics prep content (unverified).
**What the interviewer is checking:** Whether you use a comparison group (difference-in-differences) and recognise selection bias and regression to the mean.
**Say this in the interview:** "Treated attrition fell 6 points, but others fell 2 points anyway, so the bonus effect is about 4 points, roughly 12 fewer exits out of 300, with a wide margin of error. I would then test whether the groups are really comparable."
**Clarify first:** How were the 300 chosen (flight risk, manager choice)? When were bonuses paid, with what lock-in? Did anything else change (market, appraisals)?
**Structure:** Naive before-after, then difference-in-differences, then robustness against selection, then cost versus benefit.
**What I would check, in order:** 1) Naive effect: 9% - 15% = -6 points. 2) Comparison trend: 10% - 12% = -2 points. 3) Difference-in-differences = -6 - (-2) = -4 points. 4) Counterfactual treated attrition = 15% - 2 = 13%; fewer leavers = 300 x (13% - 9%) = 12 (naive reading says 18). 5) Rough uncertainty: standard error about 3 points, so 95% interval about -10 to +2 points: not conclusive. 6) Match on tenure, rating, pay, manager; check pre-trends over several periods.
**If the data shows...:** Pre-trends were parallel and effect holds after matching: credible. Bonus recipients were selected because they were about to leave: effect may be biased either way. Attrition returns after the lock-in ends: only delayed exits.
**Numeric work (if data given):** Above. Bonus pays off only if 12 avoided exits x replacement cost exceeds bonus spend; at an assumed 6 lakh per exit that is INR 72 lakh.
**Recommendation:** Call it promising, not proven; extend follow-up, randomise the next wave, and track retention after the lock-in.
**Likely follow-ups:** 1) *Why not a t-test?* Groups differ at baseline. 2) *Regression to the mean?* Groups chosen after a high-attrition spell would fall anyway.
**Common mistakes / traps:** Crediting the full 6 points; ignoring the 2-point trend; ignoring selection; reading a small sample precisely.

### Q49 ⭐⭐ 🔴 In a pay equity regression, grade is a control, but promotions to higher grades are themselves slower for women. What problem does that create and how do you handle it?
**Asked at:** commonly asked (no company-specific report found); adjusted pay-gap regression pitfalls appear in pay-equity prep content (unverified).
**What the interviewer is checking:** Whether you recognise a "bad control" (a variable that is itself affected by the thing you study) and know how to separate pay from promotion effects.
**Say this in the interview:** "If women are promoted more slowly, grade already carries part of the gender effect. Controlling for it shrinks the gap and can hide the real unfairness, so I would report both the adjusted gap and the promotion gap."
**Explain simply:**
- A control is meant to remove differences that are fair (experience, role). Grade is partly an outcome of the process we are auditing.
- With grade included, the model compares women and men only inside the same grade, so any unfairness in who got promoted disappears from the estimate.
- Example from the pay-gap question: 15.5% raw gap falls to 2% with grade. The 13.5 points that "disappeared" might be real, caused by slower promotion.
**What to do:**
1) Run models in layers: no controls; legitimate controls only (tenure, performance, location, skill); then add grade. Show how the gender coefficient changes.
2) Analyse promotion separately: time to promotion by gender with survival analysis (Kaplan-Meier), or a logistic model for promotion given performance and tenure.
3) Use a decomposition (Oaxaca-type): the gap explained by differences in characteristics versus unexplained.
4) Use salary on log scale so the coefficient reads as a percentage gap.
**Practice step:** Rerun the earlier example with grade distribution held equal and see the gap.
**Likely follow-ups:** 1) *Do you then drop grade?* Keep both views and explain which question each answers. 2) *Legal angle?* Involve counsel; findings can create obligations.
**Common mistakes / traps:** Treating the adjusted 2% as "the answer"; adding every available variable as a control; ignoring small groups.

### Q50 ⭐⭐ 🔴 Leadership wants to cut payroll by 10% through layoffs. How would you design an analysis to support selection while avoiding bias and legal risk?
**Asked at:** commonly asked (no company-specific report found); layoff and restructuring analysis appears in people-analytics prep themes (unverified).
**What the interviewer is checking:** Judgement: use objective, job-related criteria, test for adverse impact, protect confidentiality, and involve legal and HR leadership.
**Say this in the interview:** "I would first size the target, then define role-based and criteria-based selection that is job-related, run an adverse-impact check on the resulting list, and involve legal before anything is final. I would also show alternatives to layoffs."
**Clarify first:** Is 10% of payroll or of headcount? Time frame? Which functions are protected? What are local notice and severance rules? Who signs off?
**Structure:**
- Size: illustrative payroll INR 100 crore, average CTC 12 lakh (assumed): 10% = INR 10 crore, about 83 roles at average cost (fewer if senior roles are cut). Severance of 3 months (assumed) costs about INR 2.5 crore, so payback is about 3 months.
- Alternatives: hiring freeze, attrition, contractor cuts, pay deferrals, redeployment.
- Selection: first roles (work that is no longer needed), then people within roles using documented criteria.
**What I would check, in order:** 1) Role-level demand and cost. 2) Criteria: skills, recent performance over a stable period, critical skills retention; never age, gender, pregnancy, disability or union role. 3) Adverse-impact check: selection rate for each protected group divided by the highest group's rate; below 0.80 is a flag. 4) Review of flagged cases with legal and HR. 5) Document every rule before looking at names.
**If the data shows...:** A group is hit disproportionately: test whether a job-related reason holds, adjust criteria, not the evidence. Performance ratings are inconsistent across managers: calibrate first.
**Recommendation:** Deliver a rule-based, auditable shortlist plus an impact report, with restricted access to the data and legal sign-off. Measure after: regretted exits, morale, workload.
**Likely follow-ups:** 1) *Use a model to pick people?* Not as the decider; models add bias risk. 2) *Who sees the data?* Minimal access.
**Common mistakes / traps:** Choosing names first and criteria afterwards; ignoring protected-group impact; underestimating severance; leaking data.

### Q51 ⭐ 🟢 What is internal mobility rate, and what would a low rate suggest?
**Asked at:** commonly asked (no company-specific report found); internal mobility is a standard talent metric in HR metric guides (unverified).
**What the interviewer is checking:** A clear definition and a sensible reading of a low value.
**Say this in the interview:** "It is the share of employees who moved to a new role inside the company in a period. Low can mean limited growth paths, poor visibility of openings or managers blocking moves, and I would check which."
**Explain simply:**
- Internal mobility rate = employees who changed role internally (promotion or transfer) in the period / average headcount x 100.
- Example: 45 promotions + 25 lateral moves = 70; average headcount 1,000; rate = 7%.
- Related: internal fill rate = internal hires / all hires. If 70 roles went to internal staff and 230 to outsiders, it is 70 / 300 = 23.3%.
- Low rate suggests: few openings posted internally, hidden barriers (managers hoarding talent), skill gaps, or a company so stable that roles rarely open. A very low rate often goes with higher exits of ambitious people.
**Short practice step:** Split the rate by tenure, function and manager. See if people leave after 2 years without any move.
**Likely follow-ups:** 1) *Is high always good?* No, too many moves disrupt teams. 2) *Include promotions?* Say which definition you use.
**Common mistakes / traps:** Not stating the definition; dividing by closing headcount without saying; calling a low rate "bad" without a benchmark.

### Q52 ⭐ 🟡 Performance ratings given by different managers have very different distributions (some give 70% top ratings, some 10%). How would you calibrate them before using ratings in an attrition or pay analysis?
**Asked at:** commonly asked (no company-specific report found); rating calibration is a differentiator topic in people-analytics prep (unverified).
**What the interviewer is checking:** Whether you separate manager leniency from true performance before using ratings in a model.
**Say this in the interview:** "I would not use raw ratings. I would adjust for each manager's leniency, for example by standardising within manager, or better, check against objective output, and run a calibration meeting before locking the data."
**Explain simply:**
- Leniency: some managers give most people top ratings; a 4 from a tough rater is worth more than a 4 from a lenient one.
- Method 1, standardise: z-score = (rating - manager mean) / manager standard deviation. Example: manager A mean 4.2, sd 0.5, rating of 4 gives -0.4; manager B mean 2.8, sd 0.6, same rating gives +2.0. Same label, very different standing.
- Method 2, percentile rank within manager or within peer group.
- Method 3, a mixed-effects model with manager as a random effect.
- Check against objective measures (sales, quality, output). Use caution when teams really differ in quality; standardising by force can punish a genuinely strong team. Small teams (under 8) give unstable z-scores.
**Short practice step:** Compute the z-score by manager in Excel and compare which employees change top-quartile status.
**Likely follow-ups:** 1) *Why not forced distribution?* Unfair for strong small teams. 2) *Use both?* Yes, model both raw and adjusted ratings.
**Common mistakes / traps:** Using raw ratings in attrition models; z-scoring tiny teams; assuming all teams are equally strong.

### Q53 ⭐ 🟡 A quick-commerce company has 10,000 delivery partners who each started in a given week. Weekly active retention is 70% at week 4 and 45% at week 12. How do you analyse delivery-partner attrition and what levers would you test?
Inline data: week-4 active retention 70%; week-12 active retention 45%.
**Asked at:** commonly asked (no company-specific report found); gig-workforce retention is a gap-filled theme, not a reported question (unverified).
**What the interviewer is checking:** Cohort retention curves, hazard thinking, and testable levers.
**Say this in the interview:** "Of 10,000 starters, 7,000 are active at week 4 and 4,500 at week 12. Most of the loss is early: about 8.5% of the remaining partners drop each week early on, falling to about 5.4% later, so I would focus on onboarding and the first month."
**Clarify first:** What counts as "active" (one delivery a week)? Are cohorts by city? Is churn voluntary or deactivation? Is there seasonality, such as festivals or rain?
**Structure:** Cohort retention curve, then weekly hazard (share of those still active who drop that week), then segments, then levers.
**What I would check, in order:** 1) Weeks 0 to 4: 70% retained, a 30% loss (3,000 partners); weekly drop about 1 - 0.70^(1/4) = 8.5%. 2) Weeks 4 to 12: 4,500 / 7,000 = 64.3% retained over 8 weeks; weekly drop about 1 - 0.643^(1/8) = 5.4%. 3) Cut by city, vehicle owned, referral versus ad source, first-week earnings, joining incentive. 4) Survival curve by segment.
**If the data shows...:** Churn spikes after first low-earning week: earnings and order allocation problem. Referral cohorts retain better: shift acquisition spend. Churn is high among part-timers by design: judge by active hours, not heads.
**Numeric work (if data given):** Above; absolute active counts 7,000 and 4,500.
**Recommendation:** Run A/B tests: first-month earnings guarantee, onboarding training, slot choice, referral bonus. Measure week-4 and week-12 retention and cost per retained partner.
**Likely follow-ups:** 1) *Why a falling hazard?* Early leavers were poor fits. 2) *How judge incentives?* Compare cost against replacement cost.
**Common mistakes / traps:** Averaging all cohorts; calling week-12 retention "attrition rate"; ignoring that "active" is a definition.

### Q54 ⭐ 🟡 A company is considering replacing 50 permanent roles costing INR 10 lakh each with contract staff billed at INR 12 lakh each with no separate benefits cost. How do you compare the true costs?
Inline data: permanent CTC INR 10 lakh; benefits and overhead assumed an additional 20% of CTC; contract rate INR 12 lakh; replacement and onboarding costs are not given and should be listed as extra factors.
**Asked at:** commonly asked (no company-specific report found); contract versus permanent cost comparison appears in HR finance cases (unverified).
**What the interviewer is checking:** Whether you compare fully loaded costs, notice the near-tie, and list one-off and hidden factors.
**Say this in the interview:** "Permanent staff cost 10 lakh plus 20% overheads, so 12 lakh each, exactly the contract rate. The direct costs tie at INR 6 crore a year for 50 roles, so the decision turns on one-off and hidden costs."
**Clarify first:** Is the 20% reliable? Contract length? Who owns equipment, training and attrition risk?
**Structure:** Annual run-cost, then one-off costs, then non-cost factors.
**What I would check, in order:** 1) Permanent: 50 x 10 = 500 lakh; plus 20% = 600 lakh = INR 6 crore. 2) Contract: 50 x 12 = 600 lakh = INR 6 crore. 3) Difference: zero. 4) One-offs of the switch: severance and notice for 50 permanent staff (assumed 3 months of CTC, 2.5 lakh each = 125 lakh), knowledge loss, onboarding contractors. 5) Ongoing: contractor turnover and re-onboarding, vendor management, risk of lost know-how, culture and compliance risk, flexibility to scale down (a real benefit).
**If the data shows...:** Workload is temporary or uncertain: contract may win on flexibility. Work is long-term and knowledge heavy: permanent wins because the switch only adds one-off cost with zero run-cost saving.
**Numeric work (if data given):** Run cost 6.00 crore versus 6.00 crore. Illustrative one-off of 1.25 crore for severance means the first-year cost of switching is 1.25 crore higher (all assumed).
**Recommendation:** Do not switch for cost reasons alone; renegotiate the contract rate (breakeven is 12 lakh) or limit contracts to variable-demand work.
**Likely follow-ups:** 1) *What if the contract rate were 11 lakh?* Saves 50 lakh a year. 2) *Does 20% overhead include everything?* Verify.
**Common mistakes / traps:** Comparing 10 lakh against 12 lakh; forgetting the overhead; ignoring one-off severance.

### Q55 ⭐ 🟡 How do you build an HR metrics dictionary so that attrition and headcount mean the same thing across teams?
**Asked at:** commonly asked (no company-specific report found); a metrics dictionary is a listed theme in people-analyst question banks (unverified).
**What the interviewer is checking:** Governance thinking: one agreed definition, owner and source for each metric.
**Say this in the interview:** "I would write one page per metric with the formula, denominator, inclusions and exclusions, source system, owner and refresh date, get HR, finance and business heads to sign it off, and publish one certified table so everyone uses the same numbers."
**Explain simply:**
- Why it matters: with 13 leavers in a month, using opening headcount (480) gives 2.71%; closing (520) gives 2.50%; average (500) gives 2.60%. Same facts, three answers.
- What each entry holds: name, plain definition, formula, denominator, include or exclude rules (contractors, interns, notice-period staff, internal transfers, retirements), time window, data source, owner, last reviewed.
- Steps: 1) List the 15 to 20 most used metrics. 2) Collect the definitions currently in use. 3) Agree one and write it down. 4) Implement it once in a shared view or Power BI model. 5) Version-control changes. 6) Run monthly reconciliation of headcount between HR and finance.
**Short practice step:** Write the dictionary entry for attrition, including whether voluntary and involuntary exits count.
**Likely follow-ups:** 1) *What if teams disagree?* Escalate to a metric owner. 2) *Historical numbers?* Restate and flag.
**Common mistakes / traps:** Defining metrics but not the data source; ignoring contractors; letting each dashboard recompute its own version.

### Q56 ⭐ 🔴 How would you evaluate whether a new employee learning-and-development programme paid back its INR 80 lakh cost?
Inline data: programme cost INR 80 lakh; 800 participants; outcomes available: ratings, promotions, attrition, and project billing.
**Asked at:** commonly asked (no company-specific report found); learning-programme ROI is a differentiator topic (unverified).
**What the interviewer is checking:** Whether you define payback in money, build a comparison group, and avoid crediting everything to the programme.
**Say this in the interview:** "The cost is INR 10,000 per participant. I would compare participants with similar non-participants on ratings, promotions, attrition and billing, convert the difference to rupees, and check if it exceeds 80 lakh."
**Clarify first:** How were participants chosen? What is the time horizon (6 to 12 months)? How is billing attributed per person? What decision follows?
**Structure:** Cost, benefits by outcome, comparison design, ROI, caveats.
**What I would check, in order:** 1) Cost per head = 80 lakh / 800 = INR 10,000. 2) Break-even attrition: if a leaver costs 6 lakh to replace (assumed, 50% of a 12 lakh CTC), the programme pays back if it prevents 80 / 6 = 13.3, so about 14 exits. 3) Break-even billing: extra INR 10,000 of billing margin per participant. 4) Compare participants with matched non-participants (same grade, tenure, rating, project) or use before-and-after with a control group (difference-in-differences). 5) Compare ratings, promotion rate, attrition, billing.
**If the data shows...:** Participants did better but were already high performers: selection effect, not the programme. Benefits appear but only in one outcome: judge on money value of that outcome. Only ratings rise: soft benefit, no payback.
**Numeric work (if data given):** ROI = (benefit - cost) / cost. If measured benefit were INR 1.2 crore, ROI = (120 - 80) / 80 = 50% (illustrative).
**Recommendation:** Report payback with a range, say what portion is credited to the programme, and run the next cohort with a waitlist as a control.
**Likely follow-ups:** 1) *Time horizon?* Benefits may take over a year. 2) *Intangibles?* Report separately.
**Common mistakes / traps:** Comparing volunteers with non-volunteers; counting all billing growth; ignoring participants' time cost.

### Q57 ⭐ 🔴 What bias risks arise in using AI or resume-screening models in hiring, and how would you audit one for adverse impact?
**Asked at:** commonly asked (no company-specific report found); bias in hiring algorithms and adverse-impact checks appear in prep content (unverified).
**What the interviewer is checking:** Awareness of how bias enters (training data, proxies) and a concrete audit using selection-rate ratios.
**Say this in the interview:** "A model trained on past hiring learns past bias, so I would audit selection rates by group, check the four-fifths ratio, test for proxy variables and run fairness tests before and after deployment, with a human review path."
**Explain simply:**
- Bias sources: historical labels (who was hired before), proxies (college, postcode, gaps in work history, name, hobbies standing in for gender or caste), skewed training data, features such as resume wording, and feedback loops (model picks similar people, then trains on them).
- Audit steps: 1) Get applicant-level outputs with group labels held separately for testing. 2) Selection rate per group. 3) Impact ratio = lower group's rate / higher group's rate; below 0.80 is a flag (a rule of thumb). 4) Significance test. 5) Look at features and swap tests (change only the name or gender cue). 6) Check error rates by group. 7) Document and re-audit regularly.
**Worked mini-example (illustrative):** Model advances 200 of 500 men (40%) and 72 of 300 women (24%). Impact ratio = 24 / 40 = 0.60, below 0.80. Test statistic about 4.6, so unlikely to be chance. Next: check if job-related scores explain the gap, and remove or retrain on proxy features.
**Practice step:** Compute impact ratios by group and stage in Excel from a screened-versus-advanced table.
**Likely follow-ups:** 1) *Is the 0.80 rule enough?* No, it is a flag, not proof either way. 2) *Remove gender from inputs?* Not enough because proxies remain.
**Common mistakes / traps:** Auditing only accuracy; assuming removing protected fields removes bias; no human override; auditing once.


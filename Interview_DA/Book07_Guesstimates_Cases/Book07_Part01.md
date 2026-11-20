# Book 7 — Guesstimates, Case Studies & Business Metrics | Part 1: Guesstimate Framework and India Population Base Numbers 🟢🟡

**Target:** 30 questions | **Actual:** 32 questions
**Scope:** how to structure a guesstimate (top-down, bottom-up, driver trees), how to sanity-check it, and the India population base numbers used as anchors; full market-size and revenue estimates belong to Parts 2-3.

### Q1 ⭐⭐⭐ 🟢 What is a guesstimate question, and why do data analyst interviewers ask it?
**Asked at:** guesstimates are reported for Mu Sigma, Fractal, Flipkart and Meesho analyst rounds (candidate and prep-site reports, unverified); otherwise commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can turn a vague "how many" question into a structured, defensible number without data in front of you.
**Say this in the interview:** "A guesstimate is a structured estimate of something nobody has exactly measured. I will clarify, break it into parts, state assumptions out loud, calculate, then sanity-check."
**Explain simply:**
- A guesstimate (guess plus estimate) asks for a number such as "how many chai cups are sold in Pune in a day" when no one can look it up.
- It is not a wild guess: you split the number into smaller pieces you can reason about, multiply them, and say why each piece is reasonable.
- Analysts face this daily: a manager asks "how many new joiners will we need next year?" before any data is pulled. A quick, reasoned estimate sets the scale, tells you if a later report looks broken, and shows you think in drivers.
- Interviewers use it to see structure, comfort with numbers, business sense and how you react when challenged. The final figure matters least.
**Mini-example:** "Employees in a 5,000-person company who take leave on a Monday": 5,000 x (assumed 4% absent) = about 200. The logic is the answer, not the exact 200.
**Practice step:** Estimate one everyday count a day (for example, lifts in your office building) and write the assumptions down.
**Likely follow-ups:** 1) *Is there a right answer?* Usually no single one; a reasoned answer within the same order of magnitude is the goal. 2) *Why not just say "I don't know"?* Because the job is to make decisions with incomplete data.
**Common mistakes / traps:** Jumping to a number with no structure; treating it as a memory test of statistics; going silent while thinking.

### Q2 ⭐⭐⭐ 🟢 What are the standard steps you follow to solve a guesstimate question?
**Asked at:** commonly asked (no company-specific report found); prep sites describe the same steps (unverified).
**What the interviewer is checking:** That you have a repeatable method, not a one-off trick.
**Say this in the interview:** "Clarify, structure, assume, calculate, sanity-check, then summarise with a range. I will say each step aloud."
**Explain simply:**
1. **Clarify:** fix scope (which city, which time period, what counts as one unit).
2. **Structure:** choose top-down (start from a big base and cut it down) or bottom-up (build from one small unit and scale up), and draw the formula as a tree.
3. **Assume:** give each input a round number with a one-line reason; label them assumptions.
4. **Calculate:** multiply in clean steps, showing every number.
5. **Sanity-check:** use a second route or a reality check (per-person figure, known scale).
6. **Conclude:** state the answer with a range and name the assumption that matters most.
**Mini-example:** Daily absentees in a 2,000-person plant: 2,000 x 5% = 100; check: 100 per day x 22 working days = 2,200 absence-days a month, about 1.1 per person, plausible.
**Practice step:** Write these six words on a card and use them on every practice question.
**Likely follow-ups:** 1) *What if you run short of time?* Do one clean route and name the check you would run. 2) *Do you always write it down?* Yes, a visible tree helps both you and the interviewer.
**Common mistakes / traps:** Skipping clarification; hiding assumptions inside arithmetic; stopping at the number with no check.

### Q3 ⭐⭐⭐ 🟢 What is the difference between a top-down and a bottom-up guesstimate approach?
**Asked at:** commonly asked (no company-specific report found); the two approaches are standard in prep-site guides (unverified).
**What the interviewer is checking:** That you know both methods and can describe each in plain words.
**Say this in the interview:** "Top-down starts from a big total and filters it down. Bottom-up starts from one small unit and multiplies up. Ideally I do one and check with the other."
**Explain simply:**
- **Top-down:** start with a large known base (for example, a city's population) and apply shares: population x share who use it x frequency.
- **Bottom-up:** start with one unit (one tea stall, one delivery rider, one store) and scale: units x output per unit.
- Worked mini-example, daily chai cups in a city of 2 million (all inputs assumed): Top-down: 2,000,000 x 40% drinkers x 2 cups = 1,600,000 cups. Bottom-up: 4,000 stalls x 400 cups = 1,600,000 cups. Matching is luck here; the point is two independent routes.
- Top-down is quick but depends on shares that are easy to inflate; bottom-up is concrete but can miss sellers you did not count (homes, offices, cafes).
**Practice step:** Take any question and write both formulas in one line each before any numbers.
**Likely follow-ups:** 1) *Which is more accurate?* Neither by default; agreement of the two builds confidence. 2) *Can you mix them?* Yes, for example top-down demand against bottom-up supply.
**Common mistakes / traps:** Calling a one-line "population x share" bottom-up; forgetting the second route exists.

### Q4 ⭐⭐⭐ 🟢 How do you decide whether to use a top-down or a bottom-up approach for a given guesstimate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement in choosing a method, not memorised rules.
**Say this in the interview:** "I pick the route where my inputs are most believable. If the customers are everyone, top-down; if the supply is countable units, bottom-up. Then I use the other as a check."
**Explain simply:**
- Use **top-down** when the product has broad demand (phones, tea, food delivery) and the population splits naturally by age, income or city type.
- Use **bottom-up** when there are countable sellers or units with a typical output (tea stalls, hospitals, ATMs, call-centre seats).
- Ask yourself: which inputs can I defend in one sentence? Choose that route.
- Worked contrast: "Employees needing laptops in a 10,000-person firm" is top-down (10,000 x assumed 90% = 9,000). "Number of tea stalls in a city" is bottom-up (build from a typical stall or a busy lane and scale by lane count).
- If the question already names a unit (per store, per rider), that unit hints at bottom-up.
**Practice step:** For five random questions, write one line on which route you would pick and why.
**Likely follow-ups:** 1) *Can you run both?* Yes, state the second as a sanity check. 2) *What if the interviewer picks?* Follow their route first, then offer the other.
**Common mistakes / traps:** Always defaulting to population x percentage; choosing a route whose inputs you cannot justify.

### Q5 ⭐⭐⭐ 🟢 How do you sanity-check a guesstimate answer?
**Asked at:** commonly asked (no company-specific report found); sanity-check methods are described on consulting and PM prep sites (unverified).
**What the interviewer is checking:** That you test your own number instead of defending it.
**Say this in the interview:** "I check it three ways: a second route, a per-person reality check, and an order-of-magnitude look against a known scale."
**Explain simply:**
- **Second route:** estimate again top-down or bottom-up; if the two land within about 1.3x of each other (a gap of roughly 20-30%), accept.
- **Per-person or per-unit check:** divide the answer by the population or units. Example: 1.6 million chai cups across 2 million people is 0.8 cups per person per day, believable. 80 cups per person would not be.
- **Bounds:** the answer cannot exceed the total pool (cups cannot exceed people times a sane maximum) and cannot be below a floor.
- **Known scale:** compare with something you do know, for example a metro city's total daily orders or a company's reported customer count (treat reported figures as unverified).
- **Units:** check that the units cancel to what was asked.
**Practice step:** After every practice answer, write one per-person number and say yes or no.
**Likely follow-ups:** 1) *What gap is acceptable?* Within roughly 20-30% is a common convention, not a rule; an order-of-magnitude gap is a red flag. 2) *If the check fails?* Find which input is off and fix it aloud.
**Common mistakes / traps:** Using the same inputs for the "check" (circular); skipping the check when time is short.

### Q6 ⭐⭐⭐ 🟢 Why do interviewers care more about your assumptions and structure than the final number in a guesstimate?
**Asked at:** FACE Prep's Mu Sigma guide says candidates are graded on structure and assumptions (prep-site claim, unverified); otherwise commonly asked.
**What the interviewer is checking:** Whether you reason well, since the true number is unknowable here.
**Say this in the interview:** "Because the number depends on inputs nobody can verify in the room. Structure and assumptions show whether my thinking is sound and whether it can be corrected."
**Explain simply:**
- There is no answer key; two good candidates can land 30% apart and both be fine.
- A visible structure lets the interviewer test you: "what if household size is 3?" You change one input, not start over.
- Assumptions reveal business sense: assuming 100% of people order food online shows poor judgement even if the arithmetic is perfect.
- On the job, an analyst's estimate is used by others; they need the logic to trust or challenge it.
- Mini-example: a candidate who says "assumed 2 cups a day for the 40% who drink tea" can be corrected in seconds; a candidate who says "about 1.6 million" cannot.
**Likely follow-ups:** 1) *So the number does not matter?* It must be plausible (right order of magnitude), but exactness is not required. 2) *How do you show structure?* A tree and spoken labels.
**Common mistakes / traps:** Quoting a memorised statistic instead of reasoning; arguing for the number rather than the logic.

### Q7 ⭐⭐⭐ 🟢 What clarifying questions should you ask before starting a guesstimate such as "Estimate the number of chai cups sold in a city in a day"?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you fix scope before computing so you do not solve the wrong problem.
**Say this in the interview:** "I will ask about geography, time period, what counts as a cup, and who sells it, then state my scope. If there is no answer I will assume and say so."
**Explain simply:**
- **Geography:** which city, and its size? (If unspecified: "a city of about 2 million, assumed".)
- **Time:** a normal weekday, an average day, or peak season? (Average day, state it.)
- **Definition of a unit:** a cup of tea in a kulhad, a small 100 ml cup, tea at home? (Count only sold cups, not home-made.)
- **Channels:** stalls, restaurants, offices, vending machines? (Include all sold; exclude home.)
- **Purpose:** is this for supply planning or market size? It decides how precise to be.
- Then say: "Scope fixed: a city of 2 million, an average day, only cups sold, all channels."
**Practice step:** For each practice question, write the four clarifications before anything else.
**Likely follow-ups:** 1) *What if the interviewer says "your choice"?* Pick a reasonable scope and state it. 2) *How many questions?* Two to four; do not interrogate.
**Common mistakes / traps:** Asking nothing; asking ten questions; changing scope halfway.

### Q8 ⭐⭐⭐ 🟢 Which India population base numbers should a candidate memorise for guesstimates, and how should you quote them in an interview?
**Asked at:** commonly asked (no company-specific report found). Sources only support "India's population is of the order of 1.4 billion plus, urban share about a third, definitions differ" (aggregator snippets, unverified).
**What the interviewer is checking:** That you carry a few rounded anchors and are honest about their uncertainty.
**Say this in the interview:** "I use about 1.4 billion people, roughly 35% urban, about 4 to 5 people per household. These are approximate and I will say so."
**Explain simply:**
- Keep a small card (all assumed, approximate, unverified; check the latest figures before an interview):

| Anchor | Rounded value to use |
|---|---|
| Population | about 1.4 billion (140 crore) |
| Urban share | about 35% (about 50 crore people) |
| Rural share | about 65% (about 90 crore) |
| Average household size | about 4.5 (4 in cities, 5 in villages) |
| Households | about 31 crore (140 crore / 4.5 = 31.1; I round to 30 crore for easy maths) |

- Quote with a hedge: "roughly 140 crore, I will use that."
- Know the scale words: 1 lakh = 100,000; 1 crore = 10 million; 100 crore = 1 billion.
- Other states and cities: use "a metro of 1 to 2 crore" style round values.
**Practice step:** Write the table from memory twice a week; check against a current official source.
**Likely follow-ups:** 1) *What if your number is stale?* Say "approximately" and invite correction; it should not change the method. 2) *Which number matters most?* Whichever base you multiply first.
**Common mistakes / traps:** Claiming false precision (1,428,627,663); mixing crore and million; ignoring that urban/rural definitions vary.

### Q9 ⭐⭐⭐ 🟢 How do you segment India's population (for example by urban/rural, age group or income class) to start a top-down guesstimate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you slice the population into non-overlapping, collectively complete groups relevant to the product.
**Say this in the interview:** "I will split by the dimension that drives usage for this product, keep the groups non-overlapping, and make sure they add to 100%."
**Explain simply:**
- Choose the cut that matters: urban/rural for delivery apps, age for jobs or mobile games, income for premium products.
- Keep slices MECE (mutually exclusive, collectively exhaustive: no overlap, nothing missing).
- Worked example, all assumed: 140 crore people. Urban 35% = 49 crore; rural 65% = 91 crore. Within urban, assume age 18-45 is 45% = about 22 crore. Within that, assume smartphone and online-payment users are 60% = about 13 crore.
- Each cut takes you closer to "possible customers"; later cuts (income, behaviour) shrink further.
- Segments can also vary by city tier: metros, other cities, small towns.
**Practice step:** Pick a product (HR software, gym app) and decide which two cuts you would apply first.
**Likely follow-ups:** 1) *How many cuts?* Three or four; more adds error. 2) *Why not income first?* If income drives purchase, you can; relevance decides.
**Common mistakes / traps:** Overlapping slices (youth and students); percentages that do not add to 100; cutting on irrelevant dimensions.

### Q10 ⭐⭐⭐ 🟢 How do you convert India's population into a number of households, and why is household size useful?
**Asked at:** commonly asked (no company-specific report found); no reliable household count was found in the sources.
**What the interviewer is checking:** That you know when the unit of purchase is a household, not a person.
**Say this in the interview:** "Households = population / average household size. With about 140 crore people and about 4.5 per household, that is about 31 crore, which I round to 30 crore households, assumed."
**Explain simply:**
- Many purchases are per household: TV, gas connection, broadband, groceries, a car.
- Formula: households = people / people per household.
- Worked example (assumed values): 1.4 billion / 4.5 = about 311 million, roughly 30 crore after rounding. Range: at 4.0 per household, 350 million; at 5.0, 280 million.
- A smaller household size means more households for the same population, so household-based estimates rise.
- Cities have smaller households (about 4, assumed), villages larger (about 5, assumed).
**Practice step:** Convert three cities' populations to households with household sizes you choose.
**Likely follow-ups:** 1) *Does household size change over time?* It generally shrinks with urbanisation. 2) *Which is better, person or household?* Use whichever is the real buying unit.
**Common mistakes / traps:** Using households for individual products (a phone) or persons for shared ones (a fridge); dividing when you should multiply.

### Q11 ⭐⭐⭐ 🟡 Estimate the number of households in a city of 2 million people if the average household has 4 members. Show the calculation and one way to sanity-check it.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Clean arithmetic and an honest check.
**Say this in the interview:** "2 million divided by 4 is 500,000 households, about 5 lakh."
**Definition in plain words:** Households = total population / members per household.
**Worked answer:**
1. Population = 2,000,000 (given). Household size = 4 (given).
2. 2,000,000 / 4 = 500,000.
**Result:** 5 lakh households. If household size is 3.5, 571,000; at 4.5, 444,000. So a range of about 4.4 to 5.7 lakh.
**Check:** Reverse it: 500,000 x 4 = 2,000,000. Reality check: 500,000 households means about 5 lakh electricity or gas connections in the city, which fits a city of this size (assumed). A ward route: if one ward has about 10,000 people (2,500 households), 200 wards give 500,000. This only re-checks the arithmetic (it reuses household size 4), so the real independent check would be an outside count of housing or electricity connections, which I would ask for.
**Caveats:** Not everyone lives in a family household (hostels, hotels, homeless), so the true count can differ; the average hides large variation between slums and gated communities.
**Likely follow-ups:** 1) *If the interviewer says size is 5?* 400,000; the answer scales inversely. 2) *Why divide, not multiply?* Fewer, bigger groups.
**Common mistakes / traps:** Multiplying instead of dividing; dropping zeros (50,000 vs 500,000).

### Q12 ⭐⭐⭐ 🟡 Using a top-down approach, outline how you would estimate the number of people in India who could be customers of a food delivery app, without using numbers from memory beyond the population.
**Asked at:** Swiggy and Flipkart style guesstimates appear in prep-site reports (unverified); otherwise commonly asked.
**What the interviewer is checking:** A clean filter funnel from population to realistic customers, with each cut reasoned.
**Say this in the interview:** "I start from about 140 crore, filter by where delivery exists, who can pay and order, then who would try it. All the shares are my assumptions, and I get a few crore."
**Clarify first:** Who counts as a customer: ever ordered, or active monthly? I fix "could order in a month". Only India, only one app category.
**Approach:** Top-down, because food delivery has broad demand that filters by location, age and income.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 1.4 billion | given as the one number I recall |
| Live where delivery operates (large cities, bigger towns) | 30% | delivery is mostly urban |
| Age 18-45 | 45% | the main ordering age |
| Own a smartphone and pay digitally | 60% | needed to use an app |
| Can afford occasional delivery (middle income and above) | 30% | delivery costs more than cooking |

**Calculation:**
1. 1,400 million x 30% = 420 million.
2. 420 x 45% = 189 million.
3. 189 x 60% = 113.4 million.
4. 113.4 x 30% = 34 million.
**Result:** about 3.4 crore potential customers; range 2 to 5 crore.
**Sanity check:** 34 million is about 2.4% of the population, which is plausible for a premium-priced service concentrated in cities. This is a reality check, not a full second route; a true second route would be bottom-up (users x orders per user per month, compared with a city's daily order count), which I would offer if asked.
**Sensitivity:** The affordability share (30%) moves the answer most: 20% gives 22.7 million, 40% gives 45 million.
**Likely follow-ups:** 1) *Active vs potential?* Multiply by an assumed share who order monthly. 2) *Other cut?* Segment by city tier.
**Common mistakes / traps:** Using too many filters; double-counting overlapping filters (urban and affordable are correlated); using "total population" as customers.

### Q13 ⭐⭐⭐ 🟡 Using a bottom-up approach, outline how you would estimate the number of tea stalls in a city. State what unit you build from and how you scale up.
**Asked at:** commonly asked (no company-specific report found); local-business counts such as coffee shops in Bangalore appear in Mu Sigma prep guides (unverified).
**What the interviewer is checking:** Choosing a countable unit and a defensible scaling rule.
**Say this in the interview:** "I will build from one typical neighbourhood, count stalls per area, then scale by the number of such areas. For a 2 million city I get about 4,000 stalls."
**Clarify first:** Which city and size? Count only roadside stalls and small tea shops, not restaurants or cafes? I fix a city of 2 million, stalls only.
**Approach:** Bottom-up from stalls per person served in one sample area, since stalls are physical countable units. Cross-check from cups: stalls x cups per stall vs total cups.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| City population | 2,000,000 | fixed scope |
| One typical neighbourhood | 10,000 people | a ward or locality |
| Tea stalls per neighbourhood | 20 | one per 500 people in busy areas |
| Share of city that is typical | 100% | adjust for sparse suburbs |
| Cups per stall per day | 400 | same assumption as Q3 |

**Calculation:**
1. Neighbourhoods = 2,000,000 / 10,000 = 200.
2. Stalls = 200 x 20 = 4,000.
**Result:** about 4,000 stalls; range 2,900 to 5,000 (one per 700 to one per 400 people).
**Sanity check:** 4,000 stalls x assumed 400 cups = 1.6 million cups per day, which is 0.8 cups per person, plausible (the same 0.8 as the top-down chai example in Q3).
**Sensitivity:** Stalls per neighbourhood is the key input: 15 gives 3,000, 25 gives 5,000.
**Likely follow-ups:** 1) *Business districts?* Add a separate dense category. 2) *Why not top-down?* It can be the check.
**Common mistakes / traps:** Building from an unreasonable "typical" area; forgetting to account for dense versus sparse zones.

### Q14 ⭐⭐⭐ 🟡 A candidate estimates a city's daily chai consumption two ways: top-down gives 1.2 million cups, bottom-up gives 0.9 million cups. Is this gap acceptable, and what should the candidate do next?
**Asked at:** commonly asked (no company-specific report found); running both methods as a cross-check is a prep-site practice (unverified).
**What the interviewer is checking:** Judgement on tolerance and how you reconcile two estimates.
**Say this in the interview:** "The gap is 0.3 million, about 25% of the higher figure. That is acceptable for a guesstimate. I would reconcile the main assumption, then quote about 1 million with a range."
**Definition in plain words:** Gap check = (higher - lower) / higher; ratio = higher / lower.
**Worked answer:**
1. Gap = 1.2 - 0.9 = 0.3 million cups.
2. Relative to the higher number: 0.3 / 1.2 = 25%. Relative to the lower: 0.3 / 0.9 = 33%. Ratio = 1.33x.
3. Midpoint = 1.05 million; geometric mean = 1.04 million.
**Result:** About 25% of the higher figure (33% of the lower one), at the edge of the common 20-30% convention (a convention, not a rule), and well within one order of magnitude, so acceptable. Quote about 1 million cups, range 0.9 to 1.2 million.
**Check:** Per person in a 2 million city (assumed): 0.6 vs 0.45 cups per day, both plausible.
**Next steps:** Find which input is likely biased. Top-down often overstates (not everyone buys tea outside), bottom-up often understates (missed sellers: offices, restaurants). Adjust one input, reconcile, then present a single base number and a range.
**Caveats:** If the gap were 10x, something structural is wrong (a unit error); if only 5%, be wary of copying inputs between the two routes.
**Likely follow-ups:** 1) *Would you average?* Only after trying to explain the gap. 2) *What if it were 2x?* Recheck both chains for a wrong unit.
**Common mistakes / traps:** Defending one method; averaging blindly; not stating which base the 25% uses.

### Q15 ⭐⭐⭐ 🟡 What is the order-of-magnitude check, and how would you apply it to the answer "India has 5 crore (50 million) cars"?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can tell quickly if a number is off by a factor of 10 or more.
**Say this in the interview:** "Order of magnitude means the power of ten. I divide the answer by a base I know. 50 million cars over 1.4 billion people is about 1 car per 28 people, which feels slightly high; I would test it with a second route before accepting it."
**Explain simply:**
- Order of magnitude = how many zeros: thousands, lakhs, crores. Check whether your answer is in the right band, not whether it is exact.
- Method: convert to a ratio. Cars per person = 50,000,000 / 1,400,000,000 = 0.036, about 1 car per 28 people, or 3.6 per 100 people.
- Households: about 311 million (assumed 4.5 per household); 50 million cars means about 1 car for every 6 households (16%). If we assume only the top 10-15% of households can afford a car (assumed), 31 to 47 million cars would be the scale, so 5 crore is high but not absurd.
- Verdict (the 5 crore claim is an exercise input; I do not know the real count): plausible-to-slightly-high; I would test it with a second route (households with cars) rather than reject it. A claim of 50 crore would fail (1 car per 3 people).
**Practice step:** For each answer, compute a per-person or per-household ratio and ask whether it feels like an everyday observation.
**Likely follow-ups:** 1) *What do you do if it fails?* Find the broken step. 2) *Real figure?* Do not quote one from memory; I would label it unverified.
**Common mistakes / traps:** Confusing crore and million; accepting a number without any ratio; calling "too big" without a number to compare.

### Q16 ⭐⭐⭐ 🟡 How do you pick round numbers and simplify the arithmetic during a guesstimate without losing accuracy? Show it by multiplying 1.4 billion by 0.35 by 0.2 mentally.
**Asked at:** commonly asked (no company-specific report found); round numbers and spoken assumptions are advised by prep sites (unverified).
**What the interviewer is checking:** Mental speed and control over rounding error.
**Say this in the interview:** "I round to friendly numbers, round some up and some down so errors cancel, and keep the big factor exact. Here: 0.35 x 0.2 = 0.07, then 1.4 billion x 0.07 = 98 million, about 100 million."
**Explain simply:**
- Replace awkward values with simple ones (1.4 stays 1.4; 0.35 is already tidy), multiply in pairs, and track zeros separately.
- Round in opposite directions so errors tend to cancel; never round every input up.
- Worked answer:
1. 0.35 x 0.2 = 0.07 (35 x 2 = 70, then place the decimal).
2. 1.4 x 7 = 9.8, so 1.4 billion x 0.07 = 98 million.
3. Rounded: about 100 million (2% off).
- Exact value: 1,400,000,000 x 0.35 = 490,000,000; x 0.2 = 98,000,000. Matches.
- Bad rounding: turning 0.35 into 0.5 gives 140 million, 43% too high. Round only where the error is small (0.35 to 0.4 would give 112 million, 14% high; use with care).
**Practice step:** Do five three-factor products a day without a calculator, then check.
**Likely follow-ups:** 1) *How many digits?* Two significant figures is enough. 2) *When not to round?* When a tiny factor drives the answer.
**Common mistakes / traps:** Rounding all inputs the same direction; losing zeros between million and billion; over-rounding a key input.

### Q17 ⭐⭐⭐ 🔴 Two candidates estimate the daily orders of a food delivery app in a metro: one gets 20,000, the other 2,000,000. How would you find which assumption caused the 100x gap and decide which is more believable?
**Asked at:** commonly asked (no company-specific report found); guesstimates on delivery volumes are reported for Flipkart-type and Swiggy-type interviews in prep-site accounts (unverified).
**What the interviewer is checking:** Whether you debug a model by comparing driver by driver, not by defending your own number.
**Say this in the interview:** "A 100x gap is rarely small errors adding up; it is usually one driver off by 10x or two off by 10x each. I will lay both models side by side, find the first driver that differs, and test it against a per-person ratio."
**Explain simply:**
- Step 1: write both chains as drivers (city population x share who use the app x orders per user per month / 30). Compare line by line; the line with the biggest ratio is the culprit.
- Step 2: convert each answer to a per-person figure. Assuming a metro of 2 crore (20 million) people (assumed, approximate, unverified): 20,000 orders/day is 0.001 per person per day; 2,000,000 is 0.1 per person per day.
- Step 3: reality check with my own chain (all assumed): 30% of people use delivery apps = 6 million users; 3 orders per user per month = 18 million a month, about 6 lakh (600,000) a day across ALL apps. One leading app with a 40% share is about 2.4 lakh (240,000) a day. So the believable range is roughly 1 to 3 lakh.
- Step 4: test each extreme. 2,000,000 a day x 30 = 60 million a month; over all 6 million app users that is 10 orders per user per month for ONE app (25 per user if only the 2.4 million users of a 40%-share app), which is implausible as an average. 20,000 a day = 6 lakh a month, only 0.1 order per user per month, so that candidate probably forgot that most users order several times, or counted only one slice (for example one restaurant type or one area).
- Verdict: both are off, the 20,000 by about 12x low and the 2,000,000 by about 8x high against my 2.4 lakh. Say so calmly and keep the chain with the better-justified drivers.
**Likely follow-ups:** 1) *What if the gap is exactly 100x on one driver?* Then that driver is probably a unit slip (per month vs per day, or lakh vs crore). 2) *Which candidate would you hire?* The one who can explain each driver and revise it, not the one nearer my number.
**Common mistakes / traps:** Arguing for your own number; averaging the two answers; not converting to per-person; forgetting that a "per day" and "per month" mix creates a 30x error.

### Q18 ⭐⭐ 🟢 What is a decision tree or driver tree in a guesstimate, and how does it help you avoid missing a segment?
**Asked at:** commonly asked (no company-specific report found); structure and explicit assumptions are what Mu Sigma-style guesstimate rounds are reported to grade (prep-site claim, unverified).
**What the interviewer is checking:** Whether you break a big number into non-overlapping, complete pieces.
**Say this in the interview:** "A driver tree starts from the answer on top and splits it into smaller multiplications and additions, so every branch is a number I can estimate and no segment is left out."
**Explain simply:**
- A driver tree draws the answer as a root, with branches that are the things that make it up. Multiplication branches (users x orders per user) and addition branches (metro + non-metro) together cover everything.
- Good branches are MECE: mutually exclusive (no double counting) and collectively exhaustive (nothing missing).
- Example, HR: "monthly resignations" = headcount x monthly attrition rate. Split headcount by segment (freshers, mid-level, senior); each segment has its own attrition rate. If you only used one overall rate you would miss any difference between segments (for example, if freshers leave faster, which is an assumption to test).
- Example, consumer: daily orders = (users in metro + users elsewhere) x share active on a day x orders per active user.
- The check for missing segments: add the branch sizes back up; if they do not equal the parent, something is missing or counted twice.
**Practice step:** Draw a tree for "monthly cups of tea sold in a city" in two minutes, with two segments at each level.
**Likely follow-ups:** 1) *How deep should the tree go?* Until each leaf is a number you can assume in a sentence; usually 2 to 3 levels. 2) *Tree vs formula?* The formula is the tree written flat.
**Common mistakes / traps:** Overlapping branches (office workers and commuters); splitting into too many tiny segments; forgetting a big "other" segment.

### Q19 ⭐⭐ 🟢 How should you handle a guesstimate when you do not know a base number such as the population of a state?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you stay calm, say the number is an assumption, and have a method for getting close.
**Say this in the interview:** "I do not remember it exactly, so I will say my assumption out loud, get it from a nearby fact I do know, and note that I will accept a correction."
**Explain simply:**
- Never freeze and never pretend. Say "I will assume about X, tell me if it is far off."
- Method 1, scale from a known anchor: I know India is of the order of 140 crore (assumed, unverified). If a state is about one-eighth of India's size in my mind, that is about 17 to 18 crore (140 / 8 = 17.5). State it as a ratio, then ask if that sounds reasonable.
- Method 2, bracket it: "it is more than 1 crore and less than 30 crore", then pick the middle on a log scale, about 5 crore, and adjust with what you know (big or small, rural or urban).
- Method 3, build it up: number of districts x average district population (about 20 to 30 lakh, assumed).
- HR example: if you do not know a state's workforce, use state population x working-age share x employment share instead.
- Then check the final answer's sensitivity: if the answer is linear in that number, a 20% error in it is a 20% error in the answer, which is acceptable for a guesstimate.
**Likely follow-ups:** 1) *What if the interviewer gives the number?* Use theirs immediately. 2) *Is it ok to ask?* Yes, one polite question is fine; do not ask for everything.
**Common mistakes / traps:** Saying "I don't know"; stating a guess as a fact; spending two minutes on one input.

### Q20 ⭐⭐ 🟢 What are the most common mistakes candidates make in a guesstimate?
**Asked at:** commonly asked (no company-specific report found); guesstimate rounds are reported for Mu Sigma, Flipkart and Meesho (candidate and prep-site reports, unverified); this mistakes list is a synthesis, not a company-specific report.
**What the interviewer is checking:** Whether you have a checklist of failure points and avoid them.
**Say this in the interview:** "The usual failures are skipping clarifying questions, hiding assumptions, mixing units, ignoring a segment, and never sanity-checking, so I will do each of these deliberately."
**Explain simply:**
- 1) Jumping into numbers without clarifying scope (which city, what time period, which product definition).
- 2) Silent or unrealistic assumptions; always say and round them.
- 3) Unit slips: per day vs per month, lakh vs crore, per person vs per household (a 30x or 4x error).
- 4) Missing or double-counting segments (no tree).
- 5) Messy arithmetic: awkward decimals instead of round numbers, losing the thread.
- 6) No sanity check, so an impossible answer (every person orders daily) goes unnoticed.
- 7) Defensiveness when the interviewer pushes back; revise calmly instead.
- 8) Giving a bare number; also state a range and the biggest driver.
- Mini-example: 10 lakh households x 40% x 3 orders a month = 12 lakh orders a month, which is 40,000 a day (12 lakh / 30). If you forget "/30" you report 12 lakh as the daily figure, a 30x error; always label units on every line.
**Likely follow-ups:** 1) *Which one costs most marks?* Usually hidden assumptions and missing sanity checks, because the interviewer cannot follow or trust the chain. 2) *Is a wrong final number a failure?* Not if the structure and revision are good.
**Common mistakes / traps:** Treating the answer as a memory test rather than a thinking test.

### Q21 ⭐⭐ 🟡 If total population is P, the share aged 15-60 is a, the share employed in organised jobs is b, and 30% of those buy a monthly subscription, write the formula for subscribers and say which of these inputs usually carries the most uncertainty.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Chaining shares correctly and judging which input is shakiest.
**Say this in the interview:** "Subscribers = P x a x b x 0.30. Of these, b, the organised-employment share, is usually the shakiest, because definitions and data vary a lot."
**Definition in plain words:** Start with everyone, keep only the age band, keep only organised workers, then keep only those who subscribe. Each step multiplies by a share between 0 and 1. Formula: Subscribers = P x a x b x 0.30.
**Worked answer:** Illustration with assumed numbers: P = 1 crore (10 million) in a city, a = 0.6, b = 0.25 (assumed), subscription 30%. P x a = 6 million; x b = 1.5 million; x 0.30 = 450,000 subscribers.
**Result:** Formula P x a x b x 0.30; the example gives about 4.5 lakh.
**Check:** Which input carries most uncertainty: b. Halving b to 0.125 halves the answer to 225,000; doubling it to 0.5 gives 900,000. P and a are usually easier to pin down from census-type data (assumed), and the 30% was given, so b moves the answer most (relative to how little we know it).
**Caveats:** "Organised" must be defined (payroll, PF-covered, or salaried); b may be a share of the age-group or of the whole population, so state the denominator; 30% subscription is an input given in the question, not a fact.
**Likely follow-ups:** 1) *How to firm up b?* Use payroll or provident fund registration counts as a cross-check. 2) *Would you add a price filter?* Yes, only if the question says so.
**Common mistakes / traps:** Applying b to the whole population instead of the 15-60 group; mixing percentages and fractions.

### Q22 ⭐⭐ 🟡 How do you handle averages versus peak/off-peak in a guesstimate such as metro riders or delivery orders per day?
**Asked at:** commonly asked (no company-specific report found); the delivery-order and metro examples follow guesstimates reported at Flipkart and Swiggy-type interviews (prep-site accounts, unverified).
**What the interviewer is checking:** Whether you know that capacity and staffing depend on peak, not the daily average.
**Say this in the interview:** "I will give a weekly average for the daily total, then a peak-hour figure by assuming what share of the day falls in the busiest window."
**Explain simply:**
- Average answers "how many a day, overall"; peak answers "how many in the busiest hour", which decides how many riders or trains you need.
- Day types: weekday vs weekend. Assumed: weekday 1 lakh orders, weekend 1.3 lakh. Weekly average = (5 x 100,000 + 2 x 130,000) / 7 = about 1.09 lakh a day.
- Hour types: assume 30% of a weekday's orders fall in a two-hour dinner window. Peak hour = 100,000 x 0.30 / 2 = 15,000 an hour. Average over 14 active hours = 100,000 / 14 = about 7,100 an hour. So peak is about 2.1x the average.
- Rule: use the average for yearly revenue and total counts, use the peak for staffing and capacity.
- Metro riders: average daily riders from a yearly total; peak-hour load from the share travelling 8 to 10 am (also assumed).
**Practice step:** Take any estimate you made and add one line: "peak hour is about 2x the average hour."
**Likely follow-ups:** 1) *Why not use peak for everything?* It overstates totals. 2) *Seasonality?* Add a festival or monsoon multiplier to the base only if asked.
**Common mistakes / traps:** Multiplying a peak-hour figure by 24; using the weekday figure for all 7 days.

### Q23 ⭐⭐ 🟡 How do you present a range (low, base, high) rather than a single number in a guesstimate, and when is a range better? Use the example of a daily-orders estimate with a base of 100,000 and assumptions that may be 20% off in each direction.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honest uncertainty, and knowing how errors combine.
**Say this in the interview:** "My base is 100,000 orders a day; with three assumptions each possibly 20% off I would say roughly 65,000 to 135,000 as a realistic range, and 51,000 to 173,000 as the extreme range."
**Definition in plain words:** A range gives a low, base and high case. Low case = every assumption on the low side; high case = every assumption on the high side; base = your best guess.
**Worked answer:** Assume the estimate multiplies three drivers (users, active share, orders per user), each could be 20% off either way.
- One driver only: 100,000 x 0.8 = 80,000 to 100,000 x 1.2 = 120,000.
- All three low: 100,000 x 0.8 x 0.8 x 0.8 = 51,200; all three high: 100,000 x 1.2 x 1.2 x 1.2 = 172,800 (the extreme range).
- If errors are independent they partly cancel, so combined error is about 20% x square root of 3 = 35%; realistic range about 65,000 to 135,000.
**Result:** Low about 51,000 to 65,000; base 100,000; high about 135,000 to 173,000 (rounded; say "about 65 thousand to 1.35 lakh, extreme 51 thousand to 1.7 lakh").
**Check:** The base lies inside both ranges; the extreme range is wider than +/-20% because drivers multiply.
**Caveats:** A range is better when decisions depend on the size (staffing, budget) or when inputs are very uncertain; a single number is fine for a quick estimate if you also name the biggest driver. The square-root rule assumes independent errors; see Q26 on correlation. It also treats "20% off" as roughly one standard deviation (a typical miss), so the realistic range covers about two cases in three, not every case.
**Likely follow-ups:** 1) *Which number do you quote?* Quote the base and the realistic range. 2) *Why not just +/-20%?* Because errors multiply.
**Common mistakes / traps:** Adding the percentages (60% either way) or ignoring that high and low can offset each other.

### Q24 ⭐⭐ 🟡 How do you calibrate a guesstimate when you learn mid-answer that one of your assumptions is wrong (for example the interviewer says your household size is too high)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you update the number flexibly and without defensiveness.
**Say this in the interview:** "Thank you, I will switch to 4 members per household and recompute only the lines that depend on household size, so that nothing else changes by accident."
**Explain simply:**
- Step 1: accept the correction and say the new value.
- Step 2: find which lines depend on it. Household size matters only if your chain goes through households.
- Step 3: recompute. Example (assumed): city of 2 crore (20 million); at 5 per household that is 40 lakh households; x 20% order x 6 orders a month = 48 lakh a month = 1.6 lakh a day. At 4 per household: 50 lakh households; 60 lakh a month = 2 lakh a day, up 25%.
- Step 4: check whether other inputs were tuned to the old value. If "20% of households order" was chosen with 5 members in mind, a smaller household may mean fewer orders per household; mention that and adjust or flag it.
- Step 5: re-run the sanity check and say how much the answer moved.
**Practice step:** Change one input in an old estimate and see how far the answer moves.
**Likely follow-ups:** 1) *What if the chain is per person?* Nothing changes. 2) *What if the interviewer is also unsure?* Show both values.
**Common mistakes / traps:** Restarting everything; arguing; changing the input but not the dependent lines.

### Q25 ⭐⭐ 🟡 Estimate the number of working-age people in a district of 30 lakh (3 million) population if you assume roughly 60% are aged 15-59. Then say how you would adjust for a district with many young students.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A simple share calculation and thoughtful adjustment.
**Say this in the interview:** "30 lakh x 60% = 18 lakh working-age people; for a student-heavy district I would separate students from workers."
**Clarify first:** Working-age means age 15 to 59, not necessarily employed. Do you want the workforce or just the age band? I will give the age band first and then the workforce.
**Approach:** Top-down share, then adjust.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 30 lakh | given |
| Share aged 15-59 | 60% | given |
| Share aged 15-24 in a student-heavy district | 18% | assumed |
| Of them, in full-time study | 50% | assumed |

**Calculation:**
1. 30 lakh x 0.60 = 18 lakh.
2. Student-heavy: 15-24 group = 30 lakh x 0.18 = 5.4 lakh; half in study = 2.7 lakh.
3. Available workforce = 18 lakh - 2.7 lakh = 15.3 lakh.
**Result:** About 18 lakh working-age people; roughly 15 lakh available for work in a student-heavy district.
**Sanity check:** 18 lakh / 30 lakh = 0.6; the student adjustment lowers the share to 15.3/30 = 51%.
**Sensitivity:** A 5-point change in the 15-59 share moves the base by 1.5 lakh (about 8%).
**Likely follow-ups:** 1) *What if many students come from other districts?* The 15-59 share would be higher than 60%; adjust it up. 2) *Participation rate?* Apply a further share for those actually seeking work.
**Common mistakes / traps:** Calling working-age people employed; double-counting students as workers.

### Q26 ⭐⭐ 🔴 Explain the idea of independent versus correlated assumptions in a guesstimate. Why can multiplying five 'reasonable' assumptions each 20% too high give an answer that is more than 2x too high?
Hint data: 1.2 multiplied by itself 5 times.
**Asked at:** commonly asked (no company-specific report found); a gap-fill question not tied to a named source.
**What the interviewer is checking:** Whether you understand error compounding and shared bias.
**Say this in the interview:** "Errors in a multiplication chain multiply. Five inputs each 20% too high give 1.2 to the power 5 = 2.49, so the answer is about 2.5 times the true value, roughly 150% too high."
**Explain simply:**
- Independent assumptions have errors that are unrelated: some too high, some too low, so they partly cancel. Correlated assumptions share one cause (same optimistic mindset, same wrong source), so their errors lean the same way and pile up.
- Arithmetic: 1.2 x 1.2 x 1.2 x 1.2 x 1.2 = 2.49. Five inputs each 10% high give 1.1^5 = 1.61; each 20% low gives 0.8^5 = 0.33.
- Quick simulation (each input's error drawn evenly between 20% low and 20% high): if the five errors are independent, the product is above 2x only about 0.1% of the time, and 90% of the time lies between about 0.63x and 1.48x. If all five share one common error (the same optimistic mindset), the product exceeds 2x about 12% of the time. If each input leans about 12% high on average on top of its random error, it exceeds 2x about 26% of the time.
- Lesson: it is the same-direction bias, not size, that hurts. Check whether assumptions come from one mental picture (for example an affluent neighbourhood) and use round-number cross-checks.
**Likely follow-ups:** 1) *How do you reduce this?* Fewer multiplied factors and a second method. 2) *Why is a long chain risky?* Each extra factor adds error.
**Common mistakes / traps:** Adding the percentages (5 x 20% = 100% gives 2x, not 2.49x); assuming errors always cancel.

### Q27 ⭐ 🟢 How does a guesstimate differ from a market-sizing case and from a Fermi problem?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you use the terms correctly.
**Say this in the interview:** "A Fermi problem is the general idea of estimating from first principles; a guesstimate is an interview version of it, usually quick and numeric; market sizing is a business case about how big a market is, usually with a purpose such as whether to enter."
**Explain simply:**
- Fermi problem: estimate a quantity you cannot look up by breaking it into pieces you can guess (named after the physicist Enrico Fermi, for example piano tuners in a city).
- Guesstimate: the interview name for such estimates ("daily chai cups in a city"); output is a number plus the reasoning.
- Market sizing: estimating the size of a market in people or rupees, often with TAM (total addressable market), SAM (serviceable) and SOM (obtainable); it feeds a decision such as launching or investing, so it ends with a recommendation.
- Overlap: the technique is the same (drivers, assumptions, sanity checks); the difference is purpose and framing.
- Example: "How many HR software licences could be sold in India?" is market sizing; "How many people travel by metro in Delhi a day?" is a guesstimate.
**Likely follow-ups:** 1) *Are the steps different?* Almost the same, except market sizing adds a "so what" at the end. 2) *Which is harder?* Market sizing needs business judgement.
**Common mistakes / traps:** Giving a number without the decision link in market sizing; calling every estimate a Fermi problem.

### Q28 ⭐ 🟡 How would you use a known quantity (for example a company's reported number of customers) as a calibration anchor to check a guesstimate, and what are the risks?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question, not tied to a named source.
**What the interviewer is checking:** Whether you test your model against a real reference without leaning on it blindly.
**Say this in the interview:** "I will use a number I am reasonably sure about as an anchor, see whether my model reproduces it, and treat any mismatch as a clue about an assumption."
**Explain simply:**
- Calibration anchor: a known number your model should be able to reproduce, or at least be near.
- Example (exercise input, not a verified fact): suppose a delivery company reports 2 crore (20 million) customers across India. My metro model says 6 million delivery-app users (30% of 2 crore people) and a 40% share for one app = 2.4 million. If the company's national base is 20 million, that metro would be 12% of its customers while holding about 1.4% of India's people (20 million of 1,400 million). That is only plausible if delivery is heavily concentrated in the biggest metros; otherwise it is a clue that my 30% usage share is too high. If my model gave 15 million in one city, it would clearly conflict.
- Use: scale the anchor (per person, per household) to the city and compare; adjust the drivers most likely to be wrong.
- Risks: the anchor may be defined differently (registered vs active users, yearly vs monthly), may be marketing numbers, may be old, and may anchor you so strongly that you stop thinking. Also, do not tune every input just to hit the anchor; that makes the model circular.
**Likely follow-ups:** 1) *Where do anchors come from?* Reported company figures, census-type data, your own experience (for example a local shop's sales). 2) *What if there is no anchor?* Use a per-person ratio.
**Common mistakes / traps:** Treating a reported number as exact; forcing your answer to match it.

### Q29 ⭐ 🟡 How would you use units and dimensional analysis (for example orders per rider per hour) to catch an error in a guesstimate?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question, not tied to a named source.
**What the interviewer is checking:** Whether you track units to catch silly mistakes.
**Say this in the interview:** "I write the unit next to every number; if the units on the left and right do not match, the equation is wrong."
**Explain simply:**
- Units are like a spell-checker for numbers. Multiply and divide the units as you do the numbers; the result must have the unit you want.
- Example: how many riders are needed? Orders per day / (orders per rider per hour x hours per rider per day) = riders. Units: (orders/day) / [(orders/rider/hour) x (hours/day)] = riders. With 100,000 orders/day, 2 orders per rider per hour (assumed) and 6 working hours a day (assumed): 100,000 / (2 x 6) = about 8,300 riders.
- A unit error: 100,000 / 2 = 50,000 has unit "orders/day per (orders/rider/hour)", which is rider-hours a day, not riders. So the unit check catches a missing "hours per rider".
- Peak version: 15,000 orders in the peak hour / 2 orders per rider per hour = 7,500 riders on duty at peak, a different, sensible number.
- The 8,300 is an average-based floor: the fleet must also cover the peak, so the sensible size is at least the peak figure.
- Also check scale: lakh vs crore, per person vs per household.
**Practice step:** Rewrite your last guesstimate with units on every line.
**Likely follow-ups:** 1) *Does unit-checking guarantee the answer is right?* No, only that the formula is dimensionally sound. 2) *Common unit traps?* Per day vs per month, per household vs per person.
**Common mistakes / traps:** Dropping the unit after the first line; dividing when you should multiply.

### Q30 ⭐ 🟡 How would you combine supply-side and demand-side estimates to triangulate a guesstimate, using the example of cups of coffee sold per day in a city?
**Asked at:** commonly asked (no company-specific report found); a Bangalore coffee shop guesstimate is cited for Mu Sigma in the FACE Prep guide (prep site, unverified).
**What the interviewer is checking:** Triangulation: two independent routes that meet.
**Say this in the interview:** "Demand route: people who drink coffee outside the home. Supply route: outlets times cups per outlet. If they land within about 20%, I trust the answer."
**Clarify first:** Which city (assume a 1 crore, 10 million, metro), coffee only (not tea), sold outside the home, per day.
**Approach:** Both demand and supply, then compare.
**Assumptions (all assumed / approximate, unverified):**
| Input | Value | Reason |
|---|---|---|
| Population | 1 crore | assumed |
| Regular coffee drinkers | 30% | assumed |
| Cups per drinker per day | 1 | assumed |
| Share bought outside home | 25% | assumed |
| Cafes | 1,500 at 250 cups | assumed |
| Tea-coffee stalls | 5,000 at 60 coffee cups | assumed |
| Offices/vending/others | 1,000 points at 100 cups | assumed |

**Calculation:**
1. Demand: 10,000,000 x 0.30 x 1 x 0.25 = 750,000 cups.
2. Supply: cafes 1,500 x 250 = 375,000; stalls 5,000 x 60 = 300,000; others 1,000 x 100 = 100,000; total 775,000.
3. Gap: 775,000 / 750,000 = 1.03, about 3% apart.
**Result:** About 7.5 lakh cups a day (range roughly 5 to 10 lakh).
**Sanity check:** 0.075 cups per person per day, plausible for a city.
**Sensitivity:** The share bought outside home changes the demand route proportionally; a switch from 25% to 40% would raise demand to 1.2 million, which would then tell me to recheck outlet counts. Close agreement here may be partly luck; say so.
**Likely follow-ups:** 1) *What if they differ 2x?* Find the driver with the biggest uncertainty. 2) *Which route do you trust?* The one whose inputs you know better.
**Common mistakes / traps:** Using the same inputs in both routes (not independent); forgetting supply capacity limits.

### Q31 ⭐ 🟡 How should you practise guesstimates over four weeks to become fast, and what base-number cheat sheet would you build?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question, not tied to a named source (the four-week plan is the author's suggestion; no source for a prep duration was found).
**What the interviewer is checking:** Whether you have a disciplined way to improve and a ready toolkit.
**Say this in the interview:** "Four weeks: structure, then base numbers, then speed with sanity checks, then mock interviews with feedback, plus a one-page cheat sheet that I refresh weekly."
**Explain simply:**
- Week 1, structure: learn driver trees, top-down and bottom-up; do 2 guesstimates a day on paper, 10 minutes each.
- Week 2, base numbers: build the cheat sheet; practise rounding and mental arithmetic (for example 1.4 billion x 0.35 x 0.2).
- Week 3, checks and variety: add a second method and a range to each one; mix consumer, HR and logistics topics.
- Week 4, mock rounds: speak aloud with a friend or a recording, time 8 minutes, review mistakes; keep an error log.
- Cheat sheet (all assumed, approximate, unverified; verify from official sources before relying): India population about 140 crore; households about 30 crore; urban share about one-third; average household size about 4 to 5; working-age share about 60-65%; smartphone and UPI users as a share of adults; typical prices (tea Rs 10 to 20, meal Rs 150 to 300); hours per day, days per year (365, about 250 working days); an Indian city of 1 crore as a standard test city.
- Metrics of progress: time to first structure under 1 minute; answer within about 2x of a reference; assumptions stated aloud every time.
**Likely follow-ups:** 1) *How many questions in total?* About 60 to 80 over four weeks. 2) *Should I memorise numbers?* Only the small base set; understand the ratios.
**Common mistakes / traps:** Memorising answers; practising silently; building a cheat sheet from unverified numbers and never checking them.

### Q32 ⭐ 🔴 Your guesstimate for UPI transactions per day in India came out at 10 times a figure the interviewer hints at. Walk through how you would debug your own model step by step without being defensive.
**Asked at:** commonly asked (no company-specific report found); a gap-fill debugging question, not tied to a named source.
**What the interviewer is checking:** Calm, systematic debugging without defensiveness.
**Say this in the interview:** "Thanks, that tells me something is off by about 10x. I will convert both numbers to per-person terms and find which driver breaks."
**Clarify first:** What does the hinted figure measure (transactions, not value), for what period (a day), and is it approximate? (Assumed here for illustration: the hint is about 50 crore, 500 million, a day; this is an exercise value, not a verified statistic.)
**Approach:** Compare my chain with the hint step by step.
**Assumptions (all assumed / approximate, unverified):**
| Input | My model | Revised |
|---|---|---|
| Adults | 100 crore | 100 crore |
| Share who use UPI | 50% | 50% |
| Transactions per user per day | 10 | 1 |

**Calculation:**
1. My model: 1.0 billion x 0.5 x 10 = 5 billion a day, which is 3.6 per person per day across all 1.4 billion people.
2. The hint is 0.5 billion a day = 0.36 per person per day, 10x lower.
3. Test ratios: 5 billion / 0.5 billion = 10x. The gap is exactly a factor of 10, so one driver is likely 10x off; the suspect is transactions per user per day (10 vs about 1).
4. Reality check: a heavy user may do a few UPI payments a day, a light user a few a week, so an average of about 1 per user per day is a reasoned guess. Revised: 1.0 billion x 0.5 x 1 = 0.5 billion, which matches the hint; I justify the change by this reasoning, not only by the match.
**Result:** Corrected chain about 0.5 billion a day (range 0.4 to 0.7 billion, from 0.8 to 1.4 payments per user per day); my first answer was an over-count by 10x caused by the frequency assumption.
**Sanity check:** Per person 0.36 per day (about 1 payment every 3 days across everyone), plausible.
**Sensitivity:** The frequency driver; the user share matters less (30% to 70% gives 0.3 to 0.7 billion).
**Likely follow-ups:** 1) *What if frequency was right?* Then check unit (per user per month vs day) and counting rules (one payment counted twice). 2) *How do you stay non-defensive?* Say "good catch", change the number, explain the revision.
**Common mistakes / traps:** Defending the number; quietly changing three inputs at once so you cannot say what fixed it.


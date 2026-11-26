# Book 13 — Logical Reasoning & Analytical Thinking | Part 10: Quantitative-Logic Puzzles and Brain Teasers 🔴

**Target:** 50 questions | **Actual:** 54 questions
**Scope:** new-variant quantitative-logic puzzles with exact, checkable answers: weighing and measuring, ages, set counting and pigeonhole, combinatorial counting, cognitive-reflex traps and bounding/order-of-magnitude estimation, plus a few method questions on how to attack puzzles.

### Q1 ⭐⭐ 🟢 A balance scale has three possible outcomes (left heavier, right heavier, balanced). Using this, what is the minimum number of weighings needed to find the one heavier coin among 30 identical-looking coins, and why can fewer weighings never be enough?
**Asked at:** commonly asked (no company-specific report found); weighing puzzles are the classic analyst-puzzle genre (Analytics Vidhya puzzle lists, prep-site claim, unverified).
**What the interviewer is checking:** Whether you see a weighing as a 3-way information source and can turn that into a counting (information) argument.
**Say this in the interview:** "Each weighing has 3 outcomes, so k weighings can tell apart at most 3^k coins. 3^3 = 27 is less than 30 and 3^4 = 81 is enough, so the answer is 4."
**Answer:** **4 weighings.**
**Step-by-step reasoning:**
1. One weighing gives one of 3 results (left down, right down, level), so k weighings give at most 3^k different result sequences.
2. Each of the 30 coins could be the heavy one, and each possibility needs its own result sequence, so we need 3^k >= 30.
3. 3^3 = 27 < 30, so 3 weighings can never be enough. 3^4 = 81 >= 30, so 4 might work.
4. 4 does work: weigh 10 against 10. If one side sinks, the heavy coin is among those 10; if level, it is among the 10 left over. Ten coins fit within 3 weighings because 10 <= 27 (split 3, 3, 4 and continue; the 4-coin group goes 1 v 1 with 2 aside, and so on).

| Weighings | Coins that can be handled |
|---|---|
| 1 | 3 |
| 2 | 9 |
| 3 | 27 |
| 4 | 81 |

**Fast method (30 seconds):** Powers of 3: 3, 9, 27, 81. Find the first power that is at least the coin count.
**Check:** Verified by script: a dynamic programme over every possible split gives 4 for 30 coins, and 3 for 27 coins.
**Explain simply:**
- "Information argument": the number of possible answers cannot exceed the number of distinguishable outcomes of your tests.
- A balance has 3 outcomes, not 2, which is why the base is 3 and not 2.
**Likely follow-ups:** 1) *What if there were 27 coins?* Exactly 3 weighings (9 v 9, then 3 v 3, then 1 v 1; verified by script). 2) *What if the balance only showed heavier or lighter, never level?* Then the idea changes and counting is by 2^k; not needed here.
**Common mistakes / traps:** Answering with log base 2 (5 weighings) by thinking of a yes/no test; or saying 3 because 30 is "about 27".

### Q2 ⭐⭐ 🟢 A pen and a notebook together cost ₹110, and the notebook costs ₹100 more than the pen. What does the pen cost?
**Asked at:** commonly asked (no company-specific report found); a cognitive-reflex classic.
**What the interviewer is checking:** Whether you resist the instant answer (₹10) and set up the equations.
**Say this in the interview:** "The gut answer is ₹10, but then the notebook would be ₹110 and the total ₹120. Let the pen be p: p + (p + 100) = 110, so p = 5."
**Answer:** **₹5** (pen ₹5, notebook ₹105).
**Step-by-step reasoning:**
1. Let the pen cost p rupees. The notebook costs p + 100.
2. Total: p + p + 100 = 110, so 2p = 10 and p = 5.
3. Notebook = 105. Total 5 + 105 = 110, and 105 - 5 = 100. Both facts hold.
**Fast method (30 seconds):** Remove the extra ₹100 from the total: 110 - 100 = 10 is what is left for two equal "pen-sized" amounts, so one is 5.
**Check:** Verified by script (searched every amount in rupees and in paise: only ₹5 works).
**Explain simply:**
- "₹100 more than" is a difference, not a split of the total.
- The tempting answer ₹10 gives a notebook that is ₹100 more than ₹10, which is ₹110, not the stated total.
**Likely follow-ups:** 1) *Total ₹130, notebook ₹100 more?* 2p + 100 = 130, so pen ₹15 (hand-checked). 2) *Notebook costs 100 times the pen?* Not the same wording; ask which is meant.
**Common mistakes / traps:** Subtracting 100 from 110 and stopping at 10.

### Q3 ⭐⭐ 🟢 If 5 printers take 5 minutes to print 5 payslip batches, how long do 100 printers take to print 100 batches (each printer works at the same constant speed on its own batch)?
**Asked at:** commonly asked (no company-specific report found); a cognitive-reflex classic.
**What the interviewer is checking:** Working out the rate of one machine before scaling.
**Say this in the interview:** "One printer makes one batch in 5 minutes. With 100 printers and 100 batches, each prints one batch at the same time, so 5 minutes, not 100."
**Answer:** **5 minutes.**
**Step-by-step reasoning:**
1. 5 printers print 5 batches in 5 minutes, so each printer prints 1 batch in 5 minutes.
2. With 100 printers and 100 batches, give each printer its own batch.
3. All work in parallel, so everything finishes in the time one batch takes: 5 minutes.
**Fast method (30 seconds):** Ask "how long does one machine need for one job?" That time stays the same whenever machines and jobs grow together.
**Check:** Machine-minutes: 5 printers x 5 min = 25 printer-minutes for 5 batches, which is 5 printer-minutes per batch. 100 batches need 500 printer-minutes; spread over 100 printers is 5 minutes. Hand-checked.
**Explain simply:**
- A "rate" is work done per unit time by one worker. Total work = rate x workers x time.
- Machines and jobs scale together, so the time per job does not change.
**Likely follow-ups:** 1) *How long for 10 printers to print 100 batches?* 500 printer-minutes / 10 = 50 minutes (hand-checked). 2) *What if the batch cannot be split between printers and there are only 3 printers for 5 batches?* Two rounds, so 10 minutes.
**Common mistakes / traps:** Answering 100 minutes by matching the numbers 5-5-5 to 100-100-100 mechanically.

### Q4 ⭐⭐ 🟢 The number of duplicate records in a data-entry sheet doubles every day. It reached 1,024 on day 20. On which day was it 256?
**Asked at:** commonly asked (no company-specific report found); a cognitive-reflex classic.
**What the interviewer is checking:** Thinking backwards in an exponential process instead of dividing by a linear amount.
**Say this in the interview:** "It halves each step back: day 19 is 512, day 18 is 256. So day 18."
**Answer:** **Day 18.**
**Step-by-step reasoning:**
1. Doubling forward means halving backward.
2. Day 20 = 1,024; day 19 = 512; day 18 = 256.
3. 1,024 / 256 = 4 = 2 x 2, so two days earlier than day 20.
**Fast method (30 seconds):** Ratio 1,024 / 256 = 4 = 2^2, so go back 2 days.
**Check:** Verified by script: 1,024 / 2^(20 - d) = 256 only for d = 18.
**Explain simply:**
- Exponential growth means multiplying by the same factor each period; going back means dividing by that factor.
- Powers of 2 worth knowing: 2^8 = 256, 2^10 = 1,024.
**Likely follow-ups:** 1) *On which day did it reach half of 1,024?* Day 19. 2) *If it tripled each day and was 729 on day 6, when was it 81?* 729 / 81 = 9 = 3^2, so day 4.
**Common mistakes / traps:** Treating it as linear (1,024 to 256 is "3/4 less" so "many days back"), or answering day 16 by subtracting 4.

### Q5 ⭐⭐ 🟢 A courier rides from the office to a branch at 40 km/h and returns by the same road at 60 km/h. A candidate says the average speed is 50 km/h. Why is that wrong, and what is the correct average speed for the whole trip?
**Asked at:** commonly asked (no company-specific report found); a standard average-speed trap.
**What the interviewer is checking:** Knowing that average speed is total distance over total time, and that unequal times make a plain average wrong.
**Say this in the interview:** "Average speed is total distance divided by total time. He spends longer at the slow speed, so the answer is below 50. For a distance D each way: 2D / (D/40 + D/60) = 48 km/h."
**Answer:** **48 km/h** (the harmonic mean of 40 and 60, not the plain mean 50).
**Step-by-step reasoning:**
1. Pick a convenient one-way distance, 120 km (it divides by both 40 and 60). Any distance gives the same result.
2. Going: 120 / 40 = 3 hours. Returning: 120 / 60 = 2 hours. Total time 5 hours.
3. Total distance 240 km. Average speed = 240 / 5 = 48 km/h.
4. 50 is wrong because it averages the two speeds as if equal time was spent at each. But 3 hours were spent at 40 and only 2 at 60, so the slow speed counts more.
**Fast method (30 seconds):** For equal distances at speeds a and b, average = 2ab / (a + b) = 2 x 40 x 60 / 100 = 48.
**Check:** Verified by script (2 x 240 / (240/40 + 240/60) = 48).
**Explain simply:**
- "Average speed" always means total distance / total time.
- A plain average of speeds works only when equal times are spent at each speed. For equal distances use the harmonic mean (2ab / (a + b)).
**Likely follow-ups:** 1) *What if he spent equal time (not distance) at 40 and 60?* Then the average really is 50. 2) *Speeds 30 and 60 for equal distances?* 2 x 30 x 60 / 90 = 40 km/h (hand-checked).
**Common mistakes / traps:** Adding and halving the speeds; or using a different distance for each leg.

### Q6 ⭐⭐ 🟢 An employee ID is a number between 1 and 1000, and you may ask only yes/no questions. What is the minimum number of questions that guarantees you find it, and what should each question be?
**Asked at:** commonly asked (no company-specific report found); the "binary search" idea is a standard brain-teaser.
**What the interviewer is checking:** Seeing that each yes/no answer can at best halve the possibilities.
**Say this in the interview:** "Each question can at best halve the candidates. 2^10 = 1,024 is at least 1,000 and 2^9 = 512 is not, so 10 questions, each one 'is it in the lower half of what is left?'"
**Answer:** **10 questions**, each asking whether the number is in the lower half of the remaining range.
**Step-by-step reasoning:**
1. k yes/no questions give at most 2^k different answer patterns, so they can separate at most 2^k numbers.
2. 2^9 = 512 < 1000, so 9 questions are never enough. 2^10 = 1,024 >= 1000, so 10 may be enough.
3. Strategy (binary search): Q1 "Is it 500 or less?" If yes, the range is 1 to 500, otherwise 501 to 1000.
4. Keep asking "Is it in the lower half of what is left?". Ranges shrink 1000, 500, 250, 125, 63, 32, 16, 8, 4, 2, 1 (rounding up), reaching one number after 10 questions.
**Fast method (30 seconds):** Find the smallest k with 2^k >= N. Here N = 1000, k = 10.
**Check:** Verified by script: ceil(log2(1000)) = 10, and 2^9 = 512 < 1000 <= 1,024 = 2^10.
**Explain simply:**
- "Binary search" means repeatedly cutting the possible range in half.
- The same logic is why looking up a name in a sorted list takes few steps.
**Likely follow-ups:** 1) *How many for 1 to 1,000,000?* 2^20 = 1,048,576 >= 1,000,000 > 2^19, so 20 (hand-checked). 2) *What if the person may lie once?* Needs more questions; not covered here.
**Common mistakes / traps:** Asking "Is it 1? Is it 2?" (up to 999 questions); or answering 9 because 1000/2 = 500 "about 9 halvings".

### Q7 ⭐⭐ 🟢 A mother is 30 years older than her daughter. In 6 years the mother will be 4 times as old as the daughter. How old is the daughter now?
**Asked at:** commonly asked (no company-specific report found); ratio-based age items are listed in prep-site aptitude pages (prep-site claim, unverified).
**What the interviewer is checking:** Setting up one equation from "difference stays fixed, ratio changes".
**Say this in the interview:** "The age gap never changes, 30 years. In 6 years the mother is 4 times the daughter, so the gap equals 3 times the daughter's age then: 3d = 30, daughter will be 10, so she is 4 now."
**Answer:** **The daughter is 4 years old now** (mother 34).
**Step-by-step reasoning:**
1. Let the daughter be d now. Mother = d + 30.
2. In 6 years: daughter d + 6, mother d + 36.
3. Mother = 4 x daughter: d + 36 = 4(d + 6) = 4d + 24.
4. So 12 = 3d and d = 4.
**Fast method (30 seconds):** The gap (30) stays constant. If the mother is 4 times the daughter, the gap is 3 times the daughter's age: 30 / 3 = 10 in 6 years, so 10 - 6 = 4 now.
**Check:** Now 4 and 34; in 6 years 10 and 40, and 40 = 4 x 10. Verified by script (only d = 4 fits).
**Explain simply:**
- The difference between two ages is the same forever; their ratio is not.
- "Times as old" means a ratio; turn it into an equation using the fixed gap.
**Likely follow-ups:** 1) *What if the mother is 3 times the daughter in 6 years?* The gap 30 equals 2 times the daughter's age then, so she will be 15 in 6 years and is 9 now (mother 39; in 6 years 15 and 45, and 45 = 3 x 15; hand-checked). 2) *When was the mother 10 times as old?* 9d = 30 does not give a whole number of years (3.33 years old), so never at a whole age.
**Common mistakes / traps:** Forgetting to add 6 to both ages, or answering 10 (the daughter's age in 6 years).

### Q8 ⭐⭐ 🟢 What is a good routine for sanity-checking the answer to a puzzle or estimate before you say it aloud (for example extreme cases, small numbers, units, order of magnitude)? Show how it catches the error in the claim "if 3 people paint 3 walls in 3 hours, 6 people paint 6 walls in 6 hours".
**Asked at:** commonly asked (no company-specific report found); estimation guides say interviewers score structure and sanity checks, not just the number (datainterview.com, prep-site claim, unverified).
**What the interviewer is checking:** Whether you test your own answer before committing to it.
**Say this in the interview:** "I check four things: units, extreme cases, small numbers, and size. Here, one person paints one wall in 3 hours, so 6 people painting 6 walls take 3 hours, not 6."
**Answer:** **The claim is wrong: 6 people paint 6 walls in 3 hours.** The routine below catches it.
**Worked example (numbers):**
1. *Rate first (small numbers):* 3 people paint 3 walls in 3 hours, so 1 person paints 1 wall in 3 hours.
2. *Apply to the claim:* 6 people each paint their own wall at that speed, so 6 walls take 3 hours.
3. *Extreme case:* if "6 walls in 6 hours" were true, then in 6 hours 6 people would paint 6 walls, which is 1 wall per person in 6 hours, twice as slow as before. People did not slow down, so it fails.
4. *Units:* wall-people per hour: the original speed is 3 walls / (3 people x 3 hours) = 1/3 wall per person-hour. The claim gives 6 / (6 x 6) = 1/6. The rates differ, so it is wrong. (Computed by hand.)
**The routine (our suggestion):**
- **Units:** does the answer come out in the unit asked (hours, rupees, km/h)?
- **Rate per unit:** reduce to "one person, one wall" before scaling.
- **Extreme or simple cases:** try 1, 0 or a huge number; does the pattern still make sense?
- **Order of magnitude:** is the answer roughly the right size (a cup of coffee at ₹5,000 fails)?
- **Reverse substitution:** plug the answer back into the question.
**Explain simply:**
- Matching numbers (3, 3, 3 becomes 6, 6, 6) is a pattern, not a calculation.
- A 10-second check on small numbers saves a wrong answer in a live interview.
**Likely follow-ups:** 1) *How long for 1 person to paint 6 walls?* 18 hours (6 walls x 3 hours each). 2) *How many people paint 6 walls in 1 hour?* 18 (hand-checked).
**Common mistakes / traps:** Scaling every number by the same factor without checking whether time depends on the number of people.

### Q9 ⭐⭐ 🟢 You are given a puzzle you have never seen in an interview. What steps do you follow in the first two minutes, and what should you say out loud, so that the interviewer can follow your reasoning even if you do not reach the final answer?
**Asked at:** commonly asked (no company-specific report found); reports about Mu Sigma say answers must be justified aloud (FACE Prep, prep-site claim, unverified).
**What the interviewer is checking:** Your thinking process: clarifying, structuring, testing, and communicating, not just the final number.
**Say this in the interview:** "Let me restate the problem and check my assumptions. I will try a small case first, then look for a pattern, and I will tell you each step as I go."
**Answer:** **Restate, clarify, simplify, plan, then think aloud while solving and checking.** This is our suggestion, not a research finding.
**A two-minute routine (our suggestion):**
1. *0:00 to 0:20, restate:* repeat the puzzle in your own words. Name what is given and what is asked.
2. *0:20 to 0:40, clarify:* ask short questions: "Is the heavy coin always heavier? Are the ropes identical? May I use paper?" State any assumption aloud.
3. *0:40 to 1:20, simplify:* try a tiny version (2 coins, 3 people, 1 step). Look for the limiting idea: counting outcomes, a fixed difference, symmetry or parity.
4. *1:20 to 1:40, plan:* name the method before using it ("I will count possibilities", "I will work backwards").
5. *1:40 onward, solve and verify:* compute, then test the answer on an extreme case and on the original conditions.
**What to say out loud (examples):**
- "Here is what I know... here is what I need."
- "My first idea is X; let me test it on a small case."
- "That did not work because... so I will try Y."
- If stuck: "I have shown that fewer than k steps cannot work because of the counting argument; I am looking for a way to reach k." A partial result with a reason earns credit.
**Worked mini-example:** For Q1 you would say: "Each weighing has 3 outcomes, so 2 weighings tell 9 coins apart and 3 tell 27; 30 needs 4." That is a clear argument even before you describe the weighings.
**Explain simply:**
- Interviewers often care how you think more than whether you reach the answer, because on the job you will meet unfamiliar problems.
- Silence looks like being stuck; narration shows structure.
**Likely follow-ups:** 1) *You are stuck after 2 minutes: what now?* Say so, restate what you tried, and try a smaller case or work backwards from the answer. 2) *Do you ask for hints?* Yes, once you have shown your attempt; ask a specific question, not "what is the answer?".
**Common mistakes / traps:** Silently calculating, guessing a famous answer without checking, and not stating your assumptions.

### Q10 ⭐⭐ 🟢 A drawer contains 10 black, 8 blue and 6 white socks, and you pick in the dark. What is the minimum number of socks you must pick to be sure of two of the same colour?
**Asked at:** commonly asked (no company-specific report found); a pigeonhole classic.
**What the interviewer is checking:** Applying the pigeonhole principle by considering the worst case.
**Say this in the interview:** "Worst case, the first three socks are all different colours. The fourth must repeat one, so 4."
**Answer:** **4 socks.**
**Step-by-step reasoning:**
1. There are 3 colours (the "boxes"). A set of 3 socks can be all different (one black, one blue, one white).
2. So 3 socks do not guarantee a pair.
3. Any 4th sock must match one of the three colours already held, so 4 socks always contain a pair.
**Fast method (30 seconds):** Minimum to guarantee = (number of colours) + 1 = 3 + 1 = 4. The counts 10, 8 and 6 do not matter, as long as each colour has at least 2 socks.
**Check:** Verified by enumeration of all colour sequences: 3 picks can avoid a pair, 4 picks cannot.
**Explain simply:**
- Pigeonhole principle: if you place more items than boxes, some box gets at least two.
- Always plan for the worst luck, because "be sure" means no luck is allowed.
**Likely follow-ups:** 1) *How many to be sure of two of the same colour if there were 5 colours?* 6. 2) *How many to be sure of three of the same colour?* Worst case 2 of each colour = 6, so 7 (hand-checked).
**Common mistakes / traps:** Adding up the counts (answering 25 or 11), or answering 2 by assuming luck.

### Q11 ⭐⭐ 🟢 An HR database has 5 crore rows and each row takes about 200 bytes. Taking 1 GB as 10^9 bytes and 1 crore as 10^7, roughly how many GB does the table take?
**Asked at:** commonly asked (no company-specific report found); sizing and order-of-magnitude estimates are common in analytics rounds (datainterview.com, prep-site claim, unverified).
**What the interviewer is checking:** Clean unit conversion with powers of ten.
**Say this in the interview:** "5 crore is 5 x 10^7 rows. Times 200 bytes is 10^10 bytes, which is 10 GB."
**Answer:** **About 10 GB.**
**Step-by-step reasoning:**
1. Rows: 5 crore = 5 x 10^7.
2. Bytes: 5 x 10^7 x 200 = 5 x 10^7 x 2 x 10^2 = 10 x 10^9 = 10^10 bytes.
3. GB: 10^10 / 10^9 = 10 GB.
**Fast method (30 seconds):** 5 x 2 = 10, and the powers of ten add: 10^7 x 10^2 = 10^9, which is exactly 1 GB per "10 units". So 10 GB.
**Check:** Verified by script (5e7 x 200 / 1e9 = 10.0).
**Explain simply:**
- A crore is 10 million (10^7), a common Indian unit.
- This is raw size only; real databases add indexes and overhead, so the real size is usually larger (our note, not run here).
**Likely follow-ups:** 1) *If each row grew to 1 KB (1,000 bytes)?* 5 x 10^7 x 10^3 = 5 x 10^10 bytes = 50 GB. 2) *How many rows fit in 1 GB at 200 bytes?* 10^9 / 200 = 5 million.
**Common mistakes / traps:** Mixing lakh (10^5) and crore (10^7), or confusing bytes with bits.

### Q12 ⭐⭐ 🟡 Three colleagues have present ages summing to 90 years. Six years ago their ages were in the ratio 3 : 4 : 5. What is the present age of the eldest?
**Asked at:** commonly asked (no company-specific report found); ratio-based age examples are common on prep-site aptitude pages (unverified).
**What the interviewer is checking:** Adjusting for the time shift before applying the ratio.
**Say this in the interview:** "Six years ago the sum was 90 - 18 = 72. The ratio parts 3 + 4 + 5 = 12, so one part is 6: ages were 18, 24, 30. Add 6 to each: the eldest is 36."
**Answer:** **36 years** (present ages 24, 30 and 36).
**Step-by-step reasoning:**
1. Six years ago each person was 6 years younger, so the sum was 90 - 3 x 6 = 72.
2. Ratio 3 : 4 : 5 has 12 parts. One part = 72 / 12 = 6.
3. Ages then: 18, 24, 30.
4. Present ages: add 6: 24, 30, 36. Eldest = 36.

| Person | 6 years ago | Now |
|---|---|---|
| Youngest | 18 | 24 |
| Middle | 24 | 30 |
| Eldest | 30 | 36 |

**Fast method (30 seconds):** Subtract 18 from the total (3 people x 6 years), divide by 12 to get a part of 6, multiply 5 by 6 = 30, add 6.
**Check:** Present sum 24 + 30 + 36 = 90; six years ago 18 : 24 : 30 = 3 : 4 : 5. Verified by script (the only positive solution).
**Explain simply:**
- A ratio holds at one moment only. Shift everyone's age to that moment first.
- Each of the three people changed by the same 6 years, so the total changes by 3 x 6 = 18.
**Likely follow-ups:** 1) *If the ratio had been given for now and the sum was 90?* Parts 12, part = 7.5, ages 22.5, 30, 37.5 (hand-checked), a hint the question must be about the past. 2) *What was the eldest's age 6 years ago?* 30.
**Common mistakes / traps:** Splitting 90 in the ratio 3 : 4 : 5 directly (giving 37.5 for the eldest) or subtracting 6 only once instead of 18.

### Q13 ⭐⭐ 🟡 In a team, 80 know Excel, 70 know SQL and 50 know Power BI. 30 know both Excel and SQL, 20 know both SQL and Power BI, 25 know both Excel and Power BI, and 10 know all three. How many people know exactly one of the three tools?
**Asked at:** commonly asked (no company-specific report found); three-set Venn items appear in service-company aptitude tests (PrepInsta topic list, prep-site claim, unverified).
**What the interviewer is checking:** Handling overlaps carefully: "both" counts include the all-three people.
**Say this in the interview:** "The 'both' numbers include the 10 who know all three. Excel-only is 80 - 30 - 25 + 10 = 35, SQL-only is 70 - 30 - 20 + 10 = 30, Power BI-only is 50 - 20 - 25 + 10 = 15. Total 80."
**Answer:** **80 people.**
**Step-by-step reasoning:**
1. The pair counts (30, 20, 25) include the people who know all three. So people knowing exactly two of the tools = pair count - 10.
2. Exactly two: Excel and SQL only = 30 - 10 = 20; SQL and Power BI only = 20 - 10 = 10; Excel and Power BI only = 25 - 10 = 15.
3. Excel only = 80 - (20 + 15 + 10) = 80 - 45 = 35.
4. SQL only = 70 - (20 + 10 + 10) = 70 - 40 = 30.
5. Power BI only = 50 - (10 + 15 + 10) = 50 - 35 = 15.
6. Exactly one = 35 + 30 + 15 = 80.

| Region | People |
|---|---|
| Excel only | 35 |
| SQL only | 30 |
| Power BI only | 15 |
| Excel and SQL only | 20 |
| SQL and Power BI only | 10 |
| Excel and Power BI only | 15 |
| All three | 10 |

Total in the team who know at least one tool: 135.
**Fast method (30 seconds):** Exactly one = (sum of the singles) - 2 x (sum of the pairs) + 3 x (all three) = 200 - 2 x 75 + 3 x 10 = 80.
**Check:** Verified by script (region counts above; union 80 + 70 + 50 - 75 + 10 = 135). Each tool total also re-adds correctly, for example Excel: 35 + 20 + 15 + 10 = 80.
**Explain simply:**
- Draw three overlapping circles and fill from the centre outwards: all three, then exactly two, then exactly one.
- "Both A and B" includes people who also know C. That is the usual trap.
**Likely follow-ups:** 1) *How many know exactly two tools?* 20 + 10 + 15 = 45. 2) *How many know none if the team has 150 people?* 150 - 135 = 15.
**Common mistakes / traps:** Subtracting the full pair counts without adding back the all-three group, or counting Excel-only as 80 - 30 - 25 = 25.

### Q14 ⭐⭐ 🟡 Among 100 candidates, 70 know Python, 80 know SQL and 90 know Excel. What is the minimum number of candidates who must know all three?
**Asked at:** commonly asked (no company-specific report found); a classic "at least" overlap question.
**What the interviewer is checking:** Counting the people who lack a skill and bounding the overlap from below.
**Say this in the interview:** "Count who is missing each skill: 30 lack Python, 20 lack SQL, 10 lack Excel. At most 60 people lack something, so at least 100 - 60 = 40 know all three."
**Answer:** **40 candidates.**
**Step-by-step reasoning:**
1. People missing Python: 100 - 70 = 30. Missing SQL: 20. Missing Excel: 10.
2. The number of people missing at least one skill is at most 30 + 20 + 10 = 60 (it is less if the missing groups overlap).
3. So at least 100 - 60 = 40 people miss nothing, which means they know all three.
4. This minimum is reachable: let the three missing groups be completely separate (30, 20, 10 different people). Then exactly 40 people know all three.
5. Check by regions: Python and SQL only 10; Python and Excel only 20; SQL and Excel only 30; all three 40. Python total 10 + 20 + 40 = 70; SQL 10 + 30 + 40 = 80; Excel 20 + 30 + 40 = 90.
**Fast method (30 seconds):** Add the three totals and subtract (2 x population): 70 + 80 + 90 - 200 = 40.
**Check:** Verified by script (integer optimisation over all 8 regions gives a minimum of 40, with the region counts above).
**Explain simply:**
- To force an overlap, think of the complement: the people not covered by each skill.
- "Minimum" means the least overlap possible, which happens when the missing groups do not overlap at all.
**Likely follow-ups:** 1) *What is the maximum who could know all three?* 70 (everyone who knows Python also knows SQL and Excel; hand-checked). 2) *If the totals were 60, 70, 80 out of 100?* Missing 40 + 30 + 20 = 90, so at least 10 know all three.
**Common mistakes / traps:** Subtracting only one overlap (70 + 80 + 90 - 100 = 140) or answering 70 (the smallest total).

### Q15 ⭐⭐ 🟡 In a survey, 70% of employees have a graduate degree, 75% own a two-wheeler, 80% have a credit card and 85% have a mobile broadband plan. At least what percentage must have all four?
**Asked at:** commonly asked (no company-specific report found); Venn/set-counting items appear in service-MNC aptitude sections per prep sites (reported, unverified).
**What the interviewer is checking:** Whether you flip to the "missing" side and add the gaps (the union-bound idea).
**Say this in the interview:** "I count who is missing each item: 30, 25, 20 and 15 percent. Even if those groups never overlap, at most 90% miss something, so at least 10% have all four."
**Answer:** **At least 10%.**
**Step-by-step reasoning:**
1. Work with the people who lack each item: 100-70 = 30%, 100-75 = 25%, 100-80 = 20%, 100-85 = 15%.
2. The number of people lacking at least one item is largest when these four groups do not overlap at all, so it is at most 30+25+20+15 = 90%.
3. Everyone else has all four, so the all-four group is at least 100-90 = 10%.
4. It can really be 10%: put 30, 25, 20 and 15 people in four separate "missing" groups (90 people) and the other 10 have everything; the totals come out to exactly 70, 75, 80, 85.
**Fast method (30 seconds):** Minimum with all = 100 - (sum of the "missing" percentages), floored at 0. Equivalent form: (sum of the four percentages) - 300.
**Check:** Verified by script: the 100-person construction above gives 70/75/80/85 with 10 holding all four. The bound is also forced by the argument, so 10% is the exact minimum.
**Explain simply:**
- The smallest overlap happens when the "gaps" are spread so they hit different people.
- Adding gaps can overcount when groups overlap, which is why this gives a floor, not an exact value.
**Likely follow-ups:** 1) *What is the maximum with all four?* 70%, the smallest group, when everyone with a degree has the other three. 2) *Change the figures to 60, 65, 70, 75.* Gaps 40+35+30+25 = 130 is over 100, so the minimum is 0.
**Common mistakes / traps:** Multiplying percentages (0.7 x 0.75 x ... which assumes independence), or averaging them. Also forgetting to floor at 0 when the gaps add to more than 100.

### Q16 ⭐⭐ 🟡 How many integers from 1 to 500 are divisible by exactly one of 3 and 5 (that is, by 3 or 5 but not by both)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Inclusion-exclusion with the "exactly one" twist (the overlap must be removed twice).
**Say this in the interview:** "166 multiples of 3, 100 of 5, 33 of both. Exactly one means 166 - 33 plus 100 - 33, which is 200."
**Answer:** **200 integers.**
**Step-by-step reasoning:**
1. Multiples of 3 up to 500: floor(500/3) = 166. Multiples of 5: floor(500/5) = 100.
2. Divisible by both means divisible by 15 (3 and 5 share no factor): floor(500/15) = 33.
3. Only 3: 166-33 = 133. Only 5: 100-33 = 67.
4. Exactly one = 133 + 67 = 200.
**Fast method (30 seconds):** Exactly one = (A + B) - 2 x (both) = 266 - 66 = 200. "Or" (at least one) would subtract the overlap only once: 266 - 33 = 233.
**Check:** Counted by brute force over 1 to 500: 200.
**Explain simply:**
- "Divisible by" means the division leaves no remainder; floor means drop the decimal part.
- Numbers divisible by both are counted in both lists, so for "exactly one" they must be removed from both.
**Likely follow-ups:** 1) *How many are divisible by neither?* 500-233 = 267. 2) *Exactly one of 4 and 6 up to 500?* floor(500/4)=125, floor(500/6)=83, both means multiples of 12: 41; 125+83-82 = 126 (verified by the same counting rule; note the "both" number uses 12, the lcm, not 24).
**Common mistakes / traps:** Answering 233 (that is "3 or 5"), or subtracting the overlap only once. Using 3 x 5 = 15 is fine here, but for 4 and 6 you need the lcm 12, not the product.

### Q17 ⭐⭐ 🟡 A drawer contains 10 black, 8 blue and 6 white socks, and you pick in the dark. What is the minimum number of socks you must pick to be sure of at least two blue socks?
**Asked at:** commonly asked (no company-specific report found); sock-drawer pigeonhole is a classic puzzle genre.
**What the interviewer is checking:** Worst-case thinking: assume the most unlucky draw.
**Say this in the interview:** "Worst case I pull all 10 black and all 6 white first, then 1 blue, that is 17 socks with only one blue. The 18th must be blue, so 18."
**Answer:** **18 socks.**
**Step-by-step reasoning:**
1. To avoid having two blue socks as long as possible, take every non-blue sock: 10 + 6 = 16.
2. Add at most one blue sock: 17 socks, still only one blue.
3. Any 18th sock must be blue (all non-blue socks are gone), giving two blue.
4. 17 is not enough because the draw above is possible, so the minimum is 18.
**Fast method (30 seconds):** Non-target socks + (target needed - 1) + 1 = 16 + 1 + 1 = 18.
**Check:** Verified by script: the largest draw with at most one blue has 17 socks, so 18 forces two blue.
**Explain simply:**
- "Be sure" means it must work even in the unluckiest case, not on average.
- This is the pigeonhole principle: when the unlucky options run out, the next pick is forced.
**Likely follow-ups:** 1) *How many to be sure of a matching pair of any colour?* 4 (three colours, so the 4th repeats a colour). 2) *How many to be sure of two white?* 10 + 8 + 1 + 1 = 20.
**Common mistakes / traps:** Answering 10 + 2 = 12 or 2 x 3 = 6 (average-case thinking), or 17 (forgetting the last forced pick).

### Q18 ⭐⭐ 🟡 Among 85 employees, what is the largest number of them that you can be sure share the same birth month?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Pigeonhole principle with a remainder (round up, not down).
**Say this in the interview:** "12 months, 85 people. 12 x 7 = 84, so seven per month is only enough for 84; the 85th person pushes some month to 8. At least 8 are guaranteed."
**Answer:** **8 employees (guaranteed); 9 is not guaranteed.**
**Step-by-step reasoning:**
1. If every month held at most 7 people, the total would be at most 12 x 7 = 84.
2. We have 85, so some month holds at least 8.
3. 9 is not guaranteed: 1 month with 8 and 11 months with 7 gives 8 + 77 = 85, with no month above 8.
**Fast method (30 seconds):** ceiling of 85/12 = ceiling of 7.08 = 8. "Ceiling" means round up to the next whole number.
**Check:** Verified by script: ceiling(85/12) = 8 and the 8 + 11 x 7 = 85 distribution has maximum 8.
**Explain simply:**
- The principle guarantees a floor on the biggest group, not its typical size.
- A remainder (1 here) is what bumps the answer up from 7 to 8.
**Likely follow-ups:** 1) *How many people guarantee 9 in one month?* 12 x 8 + 1 = 97. 2) *How many employees are needed to guarantee two share a month?* 13.
**Common mistakes / traps:** Answering 7 (rounding down) or 7.08. The answer must be a whole number of people.

### Q19 ⭐⭐ 🟡 What is the minimum number of integers you must choose from 1 to 20 to be sure that two of them add up to 21?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Building pigeonholes (pairs) yourself.
**Say this in the interview:** "The numbers pair up as (1,20), (2,19), ... (10,11): ten pairs that each add to 21. Pick 11 numbers and two must come from the same pair. Ten is not enough, since one from each pair is safe."
**Answer:** **11 integers.**
**Step-by-step reasoning:**
1. Pair each x with 21-x: (1,20), (2,19), ..., (10,11). That is 10 pairs and every number from 1 to 20 is in exactly one pair.
2. Two chosen numbers add to 21 only if they are the two members of one pair.
3. Choosing 10 numbers can avoid this by taking one from each pair (for example 1 to 10, whose largest sum is 19).
4. A set of 11 numbers puts two in the same pair by pigeonhole, so they add to 21.
**Fast method (30 seconds):** Number of pairs + 1 = 10 + 1 = 11. The pairs are the "boxes".
**Check:** Verified by brute force over all 2^20 subsets: the largest subset with no two numbers summing to 21 has 10 members, so 11 is the minimum that forces a pair.
**Explain simply:**
- Pigeonhole needs boxes; when none are obvious, make them from the condition (pairs that add to 21).
- 21 is odd, so no number pairs with itself (10.5 is not an integer); that is why all 20 numbers fit in clean pairs.
**Likely follow-ups:** 1) *Same question with target sum 20 from 1 to 20?* Pairs (1,19) to (9,11) are 9 pairs, and 10 and 20 have no partner, so a safe set can hold 9 + 2 = 11 numbers and you need 12 (confirmed by brute force over all subsets). 2) *Target sum 21 from 1 to 30?* The numbers 21 to 30 have no partner, so a safe set can hold 10 + 10 = 20 and you need 21 (hand-reasoned the same way, not brute-forced).
**Common mistakes / traps:** Answering 20 or 19 (thinking you must take nearly everything), or 10 (forgetting one from each pair is safe).

### Q20 ⭐⭐ 🟡 How many digits does 2^100 have? Use log10(2) = 0.30103.
**Asked at:** commonly asked (no company-specific report found); digit-count questions appear in analytics-firm aptitude samples per prep sites (reported, unverified).
**What the interviewer is checking:** Using logarithms to count digits without a calculator.
**Say this in the interview:** "Digits = floor of log10 of the number, plus 1. log10(2^100) = 100 x 0.30103 = 30.103, floor 30, plus 1 gives 31 digits."
**Answer:** **31 digits.**
**Step-by-step reasoning:**
1. log10(N) tells you the power of 10 that equals N. A number with d digits satisfies 10^(d-1) <= N < 10^d, so log10(N) lies from d-1 up to just under d.
2. So digits = floor(log10 N) + 1 (floor means drop the decimals).
3. log10(2^100) = 100 x log10(2) = 100 x 0.30103 = 30.103.
4. Floor = 30, plus 1 = 31.
**Fast method (30 seconds):** Multiply the exponent by 0.30103, drop the decimals, add 1. The decimal part .103 also says the leading digits are about 10^0.103, roughly 1.27 (so 2^100 starts with 1.27).
**Check:** Verified by script with exact integer arithmetic: 2^100 = 1267650600228229401496703205376, which has 31 digits.
**Explain simply:**
- A logarithm (base 10) answers "10 to what power gives this number?"
- Each extra digit means one more factor of 10, which is one more unit in the log.
**Likely follow-ups:** 1) *Digits in 2^10?* 1024, and 10 x 0.30103 = 3.01 gives floor 3, plus 1 = 4. 2) *Digits in 3^50 given log10(3) = 0.4771?* 50 x 0.4771 = 23.855, so 24 digits (exact value checked by script: 24).
**Common mistakes / traps:** Forgetting the "+1" (answer 30), or rounding 30.103 up to 31 and thinking that is the reason (it only works by luck; the rule is floor plus 1).

### Q21 ⭐⭐ 🟡 How many digits does 5^40 × 2^30 have?
**Asked at:** commonly asked (no company-specific report found); trailing-zero and digit-count items appear in analytics-firm aptitude samples per prep sites (reported, unverified).
**What the interviewer is checking:** Pairing 2s and 5s to make powers of 10.
**Say this in the interview:** "Pair thirty 2s with thirty 5s to make 10^30. What is left is 5^10, which is 9,765,625, seven digits. So 7 + 30 = 37 digits."
**Answer:** **37 digits.**
**Step-by-step reasoning:**
1. Rewrite 5^40 = 5^10 x 5^30.
2. Then 5^30 x 2^30 = (5 x 2)^30 = 10^30.
3. So the number is 5^10 x 10^30.
4. 5^10 = 9,765,625 (7 digits). Multiplying by 10^30 adds 30 zeros: 7 + 30 = 37 digits.
**Fast method (30 seconds):** Alternative using logs: 40 x 0.69897 + 30 x 0.30103 = 27.9588 + 9.0309 = 36.99, floor 36, plus 1 = 37. The factoring route avoids needing log values.
**Check:** Verified by script with exact integers: the product has 37 digits.
**Explain simply:**
- 2 x 5 = 10, so every 2 matched with a 5 gives one zero on the end.
- The unmatched leftover (here 5^10) sets the leading digits.
**Likely follow-ups:** 1) *How many trailing zeros does it have?* 30, one per matched pair (5^10 = 9765625 ends in 5, adding none). 2) *Digits in 5^30 x 2^40?* 2^10 x 10^30 = 1024 x 10^30, which is 4 + 30 = 34 digits.
**Common mistakes / traps:** Treating it as 10^30 and answering 31, ignoring the leftover 5^10. Or the reverse near-miss of counting 5^10 as 6 digits (it is 7).

### Q22 ⭐⭐ 🟡 Without a calculator, which is larger, 12! or 2^30, and how can you decide with a quick bounding argument? (Use 2^10 = 1024 and 12! = 479,001,600 only to check.)
**Asked at:** commonly asked (no company-specific report found); estimation-and-bounding is a standard analyst brain-teaser skill (prep-site view, unverified).
**What the interviewer is checking:** Bounding with convenient powers of 2 instead of multiplying out.
**Say this in the interview:** "12! has prime factors 2^10 x 3^5 x 5^2 x 7 x 11. The part after 2^10 is below 2^8 x 2^5 x 2^3 x 2^4 = 2^20. So 12! is below 2^30."
**Answer:** **2^30 is larger.** (2^30 = 1,073,741,824 against 12! = 479,001,600, so 2^30 is about 2.2 times bigger.)
**Step-by-step reasoning:**
1. Factor 12! into primes. Powers of 2: from 2, 4, 6, 8, 10, 12 we get 1+2+1+3+1+2 = 10, so 2^10. Powers of 3: 3, 6, 9, 12 give 1+1+2+1 = 5. Powers of 5: 5 and 10 give 2. Then 7 and 11 once each. So 12! = 2^10 x 3^5 x 5^2 x 7 x 11.
2. Bound each leftover factor by a power of 2: 3^5 = 243 < 256 = 2^8; 5^2 = 25 < 32 = 2^5; 7 < 8 = 2^3; 11 < 16 = 2^4.
3. So 3^5 x 5^2 x 7 x 11 < 2^(8+5+3+4) = 2^20.
4. Therefore 12! < 2^10 x 2^20 = 2^30.
**Fast method (30 seconds):** Rough check: 12! has 9 digits (about 4.8 x 10^8) and 2^30 is about (10^3)^3 = 10^9 (since 2^10 is about 1000). 4.8 x 10^8 against 10^9 or a bit more points the same way, but it is close, so the factor bounding above is the safe proof.
**Check:** Verified by script: the prime factorisation holds, every bound above holds, and 479,001,600 < 1,073,741,824.
**Explain simply:**
- Replacing each number by a slightly bigger power of 2 gives an upper bound that is easy to add up.
- 12! (read "12 factorial") means 1 x 2 x 3 x ... x 12.
**Likely follow-ups:** 1) *Which is larger, 13! or 2^32?* 13! = 6,227,020,800 and 2^32 = 4,294,967,296, so 13! is larger (verified by script); the crossover is at 13!. 2) *Roughly how many digits does 12! have?* 9.
**Common mistakes / traps:** Trusting the rough 2^10 = 1000 estimate when the numbers are within a factor of about 2 (it can mislead), or multiplying 12 numbers by hand.

### Q23 ⭐⭐ 🟡 A deposit grows at 9% compound interest per year. What is the smallest whole number of years after which it is at least 8 times the original amount, and what does the Rule of 72 estimate instead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Compound growth with a "smallest whole number" condition, plus quick mental estimation.
**Say this in the interview:** "Solve 1.09^n >= 8, n = ln 8 / ln 1.09, about 24.13, so round up to 25 years. Rule of 72: doubling takes 72/9 = 8 years, 8x needs 3 doublings, so about 24. The exact answer is 25."
**Answer:** **25 years exactly; the Rule of 72 estimates about 24 years.**
**Step-by-step reasoning:**
1. After n years the amount is 1.09^n times the original; we need 1.09^n >= 8.
2. Take logarithms: n >= ln 8 / ln 1.09 = 2.0794 / 0.08618 = 24.13.
3. n must be a whole number of years and the condition is "at least", so n = 25.
4. Checking the neighbours: 1.09^24 = 7.911 (less than 8) and 1.09^25 = 8.623 (more than 8).
5. Rule of 72: years to double is about 72/rate% = 72/9 = 8. Eight times is 2 x 2 x 2, three doublings, so 3 x 8 = 24 years.
**Fast method (30 seconds):** Use the Rule of 72 to get 24, then test 24 and 25 years directly; since 24 falls just short (7.91), the answer steps up to 25.
**Check:** Verified by script: first n with 1.09^n >= 8 is 25.
**Explain simply:**
- Compound interest means interest is earned on past interest, so growth multiplies each year.
- The Rule of 72 is a mental shortcut (approximate, not exact); it lands within a year here because 9% is in its sweet spot.
**Likely follow-ups:** 1) *Years to double at 9% exactly?* ln 2 / ln 1.09 = 8.04, so 9 whole years (1.09^8 = 1.993, just under 2; checked by script). 2) *At what rate does money double in exactly 6 years?* About 12.2% (2^(1/6) - 1), roughly the Rule of 72 value of 12%.
**Common mistakes / traps:** Answering 24 (the estimate or rounding 24.13 down) when the question asks for at least 8 times. Also using simple interest (8 x 100/9, about 78 years).

### Q24 ⭐⭐ 🟡 A support desk receives 1,200 calls a day, each lasting 6.5 minutes on average. An agent is productive for 6 hours a day. What is the minimum number of agents needed to cover the workload?
**Asked at:** commonly asked (no company-specific report found); capacity and sizing arithmetic fits the estimation style reported for analytics interviews (unverified).
**What the interviewer is checking:** Unit conversion and rounding up for a headcount.
**Say this in the interview:** "Workload is 1,200 x 6.5 = 7,800 minutes, which is 130 hours. Each agent gives 6 hours, so 130 / 6 = 21.67. People are whole, so 22 agents."
**Answer:** **22 agents.**
**Step-by-step reasoning:**
1. Total work = 1,200 x 6.5 = 7,800 minutes.
2. In hours: 7,800 / 60 = 130 hours.
3. Agents needed = 130 / 6 = 21.67.
4. 21 agents give 126 hours (short by 4 hours), so we round up to 22 agents (132 hours).
**Fast method (30 seconds):** Convert agent time to minutes instead: 6 x 60 = 360 minutes; 7,800 / 360 = 21.67, round up.
**Check:** Verified by script: 130.0 hours of work, 21.67 agents, ceiling 22.
**Explain simply:**
- Workload divided by capacity per person gives the headcount, always rounded up.
- This ignores real-world details (peak hours, breaks, variation in call length); real planning adds a buffer, as a stated assumption.
**Likely follow-ups:** 1) *What utilisation does the desk run at with 22 agents?* 130 / 132 = about 98.5%, very tight. 2) *If you want 85% utilisation?* 130 / (6 x 0.85) = 25.5, so 26 agents (verified by script).
**Common mistakes / traps:** Mixing minutes and hours (answer 7,800/6 = 1,300), or rounding 21.67 down to 21 or to the nearest number.

### Q25 ⭐ 🟢 A person was x years old in the year x² and was born in the 20th century or earlier (the year x² lies between 1901 and 2000). In which year was the person born?
**Asked at:** commonly asked (no company-specific report found); the age-and-square-year puzzle is a classic aptitude item.
**What the interviewer is checking:** Bounding to find a unique integer, then checking the answer.
**Say this in the interview:** "The year x squared must be between 1901 and 2000. 43 squared is 1849 and 45 squared is 2025, both outside. 44 squared is 1936, so the person was 44 in 1936 and was born in 1892."
**Answer:** **Born in 1892.**
**Step-by-step reasoning:**
1. We need 1901 <= x^2 <= 2000. Since 43^2 = 1849 (too small) and 45^2 = 2025 (too big), the only integer is x = 44.
2. x^2 = 44^2 = 1936, so the person was 44 years old in 1936.
3. Birth year = 1936 - 44 = 1892.
**Fast method (30 seconds):** Square roots: sqrt(1900) is just over 43 and sqrt(2000) is just over 44.7, so only 44 fits. Always check the square of the neighbours.
**Check:** Verified by script: the only x with x^2 in 1901 to 2000 is 44, giving birth year 1892. Also hand-checked: 1936 - 1892 = 44.
**Explain simply:**
- The range condition turns an open puzzle into a one-candidate search.
- Uniqueness comes from the range: squares near 1900 to 2000 are spaced about 88 apart, so at most one lands in a 100-wide window.
**Likely follow-ups:** 1) *What if the year x^2 is allowed between 1801 and 1900?* Then x = 43 (1849), born 1806 (verified by script). 2) *Was the person alive in 1900?* Yes, 1892 to 1936 spans 1900 (age 8).
**Common mistakes / traps:** Trying x = 45 (2025, in the future of the stated range) or reporting 1936 (the year x^2) instead of the birth year.

### Q26 ⭐ 🟢 Using a balance where weights go only on one pan (the object on the other), what is the smallest number of weights needed to weigh every whole number of kilograms from 1 to 100?
**Asked at:** commonly asked (no company-specific report found); weight-set puzzles are a classic analyst-brain-teaser genre per prep sites (unverified).
**What the interviewer is checking:** Binary (powers of 2) thinking and a counting lower bound.
**Say this in the interview:** "Each weight is either on the pan or off, so n weights make at most 2^n - 1 non-zero totals. I need 100 different totals, 2^6 - 1 = 63 is too few, 2^7 - 1 = 127 is enough. So 7 weights: 1, 2, 4, 8, 16, 32, 64."
**Answer:** **7 weights, for example 1, 2, 4, 8, 16, 32, 64 kg.**
**Step-by-step reasoning:**
1. With n weights, each is either on the pan or off: 2^n ways, minus the empty choice, so at most 2^n - 1 different non-zero totals.
2. We need 100 different values (1 to 100). With 6 weights the limit is 63 < 100, so 6 can never be enough.
3. With 7 weights the limit is 127, so 7 might work, and the powers of 2 do work.
4. Why it works: every whole number has a binary form, which is exactly a choice of which powers of 2 to add. Example: 100 = 64 + 32 + 4.
**Fast method (30 seconds):** Smallest n with 2^n - 1 >= 100, and the weights are the powers of 2.
**Check:** Verified by script: subsets of {1, 2, 4, 8, 16, 32, 64} reach every integer from 1 to 127 (so 1 to 100 included), and 6 weights give at most 63 non-zero sums.
**Explain simply:**
- Binary is the number system that uses only 0 and 1 (here: weight off or on).
- Powers of 2 waste nothing because every total is reachable in exactly one way.
**Likely follow-ups:** 1) *If weights may go on both pans?* Powers of 3 (1, 3, 9, 27, 81) work, so 5 weights reach up to 121 (a standard result; hand-checked by the balanced-ternary idea, and 4 weights reach only 40). 2) *How many weights to weigh 1 to 1000 on one pan?* 10 (2^10 - 1 = 1023).
**Common mistakes / traps:** Answering 100 or 10 (one weight per decade) or 8 (rounding 100/16 up); also not proving that fewer cannot work.

### Q27 ⭐ 🟢 Two trains 100 km apart start moving towards each other on the same track at 40 km/h and 60 km/h. A bee starts on the first train and flies back and forth between the trains at 90 km/h until they meet. How far has the bee flown?
**Asked at:** commonly asked (no company-specific report found); the bee-and-trains puzzle is a famous classic.
**What the interviewer is checking:** Whether you avoid summing an infinite series and use total time instead.
**Say this in the interview:** "The trains close at 40 + 60 = 100 km/h over 100 km, so they meet after 1 hour. The bee flies the whole hour at 90 km/h, so 90 km."
**Answer:** **90 km.**
**Step-by-step reasoning:**
1. The trains approach each other at a combined speed of 40 + 60 = 100 km/h.
2. The gap is 100 km, so they meet after 100 / 100 = 1 hour.
3. The bee flies for that whole hour at a constant 90 km/h.
4. Distance = speed x time = 90 x 1 = 90 km.
**Fast method (30 seconds):** Find the total time first, then multiply by the bee's speed. It works because the bee never stops until the trains meet, so the number of back-and-forth legs does not matter.
**Check:** Verified by script: summing the bee's legs one by one (each leg shrinks by a fixed ratio, with 100 or so legs) converges to 90 km.
**Explain simply:**
- "Closing speed" is the sum of speeds when objects move toward each other.
- Distance = speed x time; the time is the only thing you need here.
**Likely follow-ups:** 1) *How far does each train travel before meeting?* 40 km and 60 km. 2) *If the bee flies at 120 km/h?* 120 km.
**Common mistakes / traps:** Setting up an infinite series of legs (it works but takes far longer), or using 90 x 100/40 because only one train's speed was used.

### Q28 ⭐ 🟡 At a party with 10 married couples, every person shakes hands once with every other person except his or her own spouse. How many handshakes take place?
**Asked at:** commonly asked (no company-specific report found); handshake-counting is a classic combinatorics warm-up.
**What the interviewer is checking:** Counting pairs and then removing the excluded pairs.
**Say this in the interview:** "20 people make 20 x 19 / 2 = 190 possible handshakes. Ten of those pairs are spouses who do not shake, so 190 - 10 = 180."
**Answer:** **180 handshakes.**
**Step-by-step reasoning:**
1. There are 10 couples, so 20 people.
2. Number of pairs of people = 20 x 19 / 2 = 190 (each person pairs with 19 others, and each pair is counted twice).
3. The 10 spouse pairs do not shake hands: 190 - 10 = 180.
4. Alternative: each person shakes 18 hands (20 - self - spouse), so total = 20 x 18 / 2 = 180.
**Fast method (30 seconds):** Per person 18 handshakes, times 20 people, divided by 2 for double counting.
**Check:** Verified by script: counting pairs of 20 people whose couple numbers differ gives 180.
**Explain simply:**
- A pair of people is one handshake, so we count pairs, not people.
- Dividing by 2 fixes the double count (A shaking B is the same as B shaking A).
**Likely follow-ups:** 1) *What if only one person in each couple takes part in handshakes (10 people, no spouses present)?* Then it is plain pairs: 10 x 9 / 2 = 45. 2) *With 8 couples?* 16 x 14 / 2 = 112 (verified by script).
**Common mistakes / traps:** Forgetting to halve (answer 360), using 20 x 19 without removing spouses (190), or removing only 20 instead of 10 spouse pairs (170).

### Q29 ⭐ 🟡 A knockout tournament has 37 players, and any odd player in a round gets a bye (advances without playing). How many matches are played in total to decide the champion, and what is the shortcut?
**Asked at:** commonly asked (no company-specific report found); knockout-count teasers are a standard analytics-interview genre (prep-site claim, unverified).
**What the interviewer is checking:** Whether you look for an invariant (something that never changes) instead of simulating round by round.
**Say this in the interview:** "Every match knocks out exactly one player, and 36 of the 37 must be knocked out, so 36 matches. Byes do not change that."
**Answer:** **36 matches.** Shortcut: matches = players - 1.
**Step-by-step reasoning:**
1. Round 1: 37 players, 18 matches, 1 bye, so 19 advance.
2. Round 2: 19 players, 9 matches, 1 bye, so 10 advance.
3. Round 3: 10 players, 5 matches, 5 advance.
4. Round 4: 5 players, 2 matches, 1 bye, 3 advance.
5. Round 5: 3 players, 1 match, 1 bye, 2 advance.
6. Round 6: 2 players, 1 match, 1 champion.
7. Total: 18 + 9 + 5 + 2 + 1 + 1 = 36.
**Fast method (30 seconds):** One champion means 36 losers. Each match produces exactly one loser (a bye produces none), so 36 matches. Why it works: the count of "players still alive" drops by exactly 1 per match and by 0 per bye.
**Check:** A short script that plays the rounds (n -> n//2 + n%2, adding n//2 matches) gives 36 for 37 players; the same code gives 63 for 64 and 32 for 33.
**Explain simply:**
- An invariant is a quantity that changes by a fixed amount each step; here "players alive" falls by 1 per match.
- A bye is a free pass, so it never changes the match count.
**Likely follow-ups:** How many matches for 64 players? 63 (checked by script). Does the number of rounds change the total? No, only the number of players matters.
**Common mistakes / traps:** Adding round by round and slipping on byes, or answering 37/2 = 18 (that is only round 1).

### Q30 ⭐ 🟡 A chocolate bar is a 6 × 8 grid of squares. Each break splits one piece along a grid line into two pieces. What is the minimum number of breaks needed to separate all 48 squares, and why does the order of breaks not matter?
**Asked at:** commonly asked (no company-specific report found); a classic of the "find the invariant" brain-teaser genre (prep-site claim, unverified).
**What the interviewer is checking:** Whether you see that each break adds exactly one piece, so the count is fixed.
**Say this in the interview:** "I start with 1 piece and need 48. Every break adds exactly one piece, so I need 47 breaks, whatever the order."
**Answer:** **47 breaks.** The order does not matter because every break raises the piece count by exactly 1.
**Step-by-step reasoning:**
1. Start: 1 piece (the whole bar). Goal: 48 single squares.
2. A break splits one piece into two, so pieces go up by exactly 1 each time.
3. To go from 1 piece to 48 pieces you need 48 - 1 = 47 breaks.
4. Nothing in this argument depends on which line you break along or in which order, so every complete plan takes exactly 47 breaks.
5. You cannot do it in fewer, because each break gains only one piece; you cannot be forced to do more, because once there are 48 pieces all are single squares.
**Fast method (30 seconds):** breaks = squares - 1 = 6 x 8 - 1 = 47. (Stacking pieces is not allowed here; each break works on one piece.)
**Check:** Arithmetic 6 x 8 - 1 = 47; the alternative plan "6 - 1 = 5 long breaks, then 6 x (8 - 1) = 42 short breaks" also totals 47, which confirms the order does not matter.
**Explain simply:**
- Invariant means "this changes by the same amount every time".
- Because the gain per break is fixed, only the target number of pieces matters.
**Likely follow-ups:** What about a 5 x 5 bar? 24 breaks (25 - 1). What if you could stack pieces and break several at once? Then fewer breaks are possible, but this question does not allow it.
**Common mistakes / traps:** Counting grid lines (5 + 7 = 12) and forgetting each line must be broken in every separate piece, or hunting for a "clever order" that saves breaks.

### Q31 ⭐ 🟡 What is the maximum number of pieces a flat circular pizza can be cut into with 6 straight cuts?
**Asked at:** commonly asked (no company-specific report found); the "lazy caterer" cut-the-pizza question is a standard brain teaser (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can build up a pattern step by step and generalise it.
**Say this in the interview:** "The nth cut can cross all earlier cuts, adding n new pieces. So pieces = 1 + 1 + 2 + ... + 6 = 22."
**Answer:** **22 pieces.**
**Step-by-step reasoning:**
1. 0 cuts: 1 piece.
2. Each new cut can cross each earlier cut once, inside the pizza. If it crosses k earlier cuts it passes through k + 1 regions and splits each into two, adding k + 1 pieces.
3. The best case is crossing every earlier cut (and no three cuts meeting at one point): the nth cut adds n pieces.
4. Pieces after cuts 1 to 6: 2, 4, 7, 11, 16, 22.
5. Formula: 1 + n(n + 1)/2 = 1 + 6 x 7 / 2 = 22.
**Fast method (30 seconds):** 1 + (1 + 2 + 3 + 4 + 5 + 6) = 1 + 21 = 22.
**Check:** Verified by script: a straight cut is a chord, two chords cross inside only if their endpoints alternate around the circle; over all 10,395 ways to pair 12 endpoints for 6 cuts, the most crossings is 15, giving 1 + 6 + 15 = 22. The same code gives 2, 4, 7, 11, 16 for 1 to 5 cuts.
**Explain simply:**
- A straight cut across a round pizza is a chord; two chords can meet at most once.
- More crossings means more pieces, so you maximise crossings.
**Likely follow-ups:** 5 cuts? 16 (script). What is the general formula? 1 + n(n + 1)/2.
**Common mistakes / traps:** Answering 12 (2 per cut), or cutting through the centre every time, which makes all cuts meet at one point and gives only 12 pieces.

### Q32 ⭐ 🟡 A child climbs a staircase of 7 steps taking 1, 2 or 3 steps at a time. In how many different ways can the child reach the top?
**Asked at:** commonly asked (no company-specific report found); a standard counting-by-recursion item (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can build a recurrence (each answer from earlier answers) instead of listing everything.
**Say this in the interview:** "The last move is 1, 2 or 3 steps, so ways(n) = ways(n-1) + ways(n-2) + ways(n-3). That gives 1, 2, 4, 7, 13, 24, 44. Answer: 44."
**Answer:** **44 ways.**
**Step-by-step reasoning:**
1. Let W(n) be the number of ways to climb n steps. Take W(0) = 1 (one way to stand still).
2. The final move was 1, 2 or 3 steps, so W(n) = W(n-1) + W(n-2) + W(n-3).
3. W(1) = 1; W(2) = 1 + 1 = 2; W(3) = 2 + 1 + 1 = 4.
4. W(4) = 4 + 2 + 1 = 7; W(5) = 7 + 4 + 2 = 13; W(6) = 13 + 7 + 4 = 24.
5. W(7) = 24 + 13 + 7 = 44.
**Fast method (30 seconds):** Write the table 1, 1, 2, 4, 7, 13, 24, 44 and add the previous three each time.
**Check:** Checked by brute force: listing every ordered sequence of 1s, 2s and 3s that sums to 7 gives 44 sequences.
**Explain simply:**
- Order matters here: 1 + 2 and 2 + 1 are different ways.
- A recurrence splits a big problem by its last step, which turns a long list into three small ones.
**Likely follow-ups:** With only 1 or 2 steps allowed? 21 (the Fibonacci pattern 1, 2, 3, 5, 8, 13, 21, checked by script). With steps 1, 2, 3 and 10 stairs? 274 by the same table (not needed here; extend 44 + 24 + 13 = 81 for 8, 149 for 9, 274 for 10).
**Common mistakes / traps:** Counting only unordered sets of steps (that gives the number of partitions, 8, not 44), or forgetting W(0) = 1.

### Q33 ⭐ 🟡 There are 100 lockers numbered 1 to 100, all closed. Student k (k = 1 to 100) toggles every k-th locker (open becomes closed, closed becomes open). After all 100 students finish, how many lockers are open and which ones?
**Asked at:** commonly asked (no company-specific report found); the 100-lockers puzzle is a widely circulated classic (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can turn a simulation into a counting argument about divisors.
**Say this in the interview:** "A locker ends open if it is toggled an odd number of times, which means it has an odd number of divisors. Only perfect squares do, so the open lockers are 1, 4, 9, ..., 100: ten of them."
**Answer:** **10 lockers are open: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100.**
**Step-by-step reasoning:**
1. Locker n is toggled by student k exactly when k divides n. So the number of toggles equals the number of divisors of n.
2. Starting closed, a locker is open at the end only if the toggle count is odd.
3. Divisors come in pairs (d, n/d). A pair gives two different divisors unless d = n/d, that is, n = d x d.
4. So the count is odd only when n is a perfect square (one unpaired divisor).
5. Perfect squares up to 100: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, which is 10.
**Fast method (30 seconds):** Open lockers = perfect squares up to 100, so floor(square root of 100) = 10.
**Check:** Checked by simulating all 100 students: exactly lockers 1, 4, 9, 16, 25, 36, 49, 64, 81 and 100 end open.
**Explain simply:**
- A divisor of n is a number that divides n exactly (divisors of 12: 1, 2, 3, 4, 6, 12).
- Pairing divisors is the core idea: 12 pairs as (1, 12), (2, 6), (3, 4), but 36 has the lone divisor 6 pairing with itself.
**Likely follow-ups:** 1000 lockers? floor(square root of 1000) = 31 open (31 x 31 = 961, 32 x 32 = 1024). Which locker is toggled most among 1 to 100? Those with most divisors, such as 60, 72, 84, 90, 96 (12 divisors each).
**Common mistakes / traps:** Thinking primes stay open (a prime has 2 divisors, so it is toggled twice and ends closed), or answering 50 from "every second locker".

### Q34 ⭐ 🟡 How many rectangles of all sizes (squares included) can be traced on an 8 × 8 chessboard grid?
**Asked at:** commonly asked (no company-specific report found); the chessboard-rectangles count is a standard combinatorics teaser (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can count a rectangle by choosing its boundary lines.
**Say this in the interview:** "A rectangle is fixed by choosing 2 of the 9 vertical lines and 2 of the 9 horizontal lines. C(9,2) x C(9,2) = 36 x 36 = 1,296."
**Answer:** **1,296 rectangles (204 of them are squares).**
**Step-by-step reasoning:**
1. An 8 x 8 board has 8 squares in a row, bounded by 9 vertical grid lines and 9 horizontal grid lines.
2. A rectangle is determined by its left and right edges (2 different vertical lines) and its top and bottom edges (2 different horizontal lines).
3. Ways to choose 2 vertical lines from 9: C(9,2) = 9 x 8 / 2 = 36. Same for horizontal.
4. Total rectangles = 36 x 36 = 1,296.
5. For interest, squares alone: 8^2 + 7^2 + ... + 1^2 = 204; so 1,296 includes 204 squares.
**Fast method (30 seconds):** (n(n + 1)/2)^2 with n = 8: 36 squared = 1,296. Also equals (1 + 2 + ... + 8)^2.
**Check:** Verified by script: looping over all pairs of grid lines in both directions gives 1,296 (36 x 36).
**Explain simply:**
- C(9,2) ("9 choose 2") means the number of ways to pick 2 items from 9 when order does not matter.
- Choosing boundary lines avoids having to count by size.
**Likely follow-ups:** A 3 x 3 grid? C(4,2)^2 = 36. A 5 x 8 board? C(6,2) x C(9,2) = 15 x 36 = 540.
**Common mistakes / traps:** Counting only squares (204), using 8 lines instead of 9 (C(8,2)^2 = 784), or answering 64.

### Q35 ⭐ 🟡 A contractor works for 15 days and must be paid one gold unit per day from a single bar of 15 units. What is the minimum number of cuts, given that the contractor can be given and can give back pieces each day?
**Asked at:** commonly asked (no company-specific report found); a classic gold-bar puzzle (prep-site claim, unverified).
**What the interviewer is checking:** Whether you see that powers of 2 can make every number (binary thinking) and can prove fewer cuts cannot work.
**Say this in the interview:** "Cut the bar into 1, 2, 4 and 8. That is 3 cuts, and any day's payment is a combination of those pieces, with exchanges as needed."
**Answer:** **3 cuts, giving pieces of 1, 2, 4 and 8.**
**Step-by-step reasoning:**
1. k cuts on a straight bar make k + 1 pieces. With p pieces the contractor can hold at most 2^p - 1 different non-empty combinations.
2. We need 15 different totals (1 to 15), so p pieces must give at least 15 combinations: 2^p - 1 >= 15, so p >= 4. That means at least 3 cuts.
3. With pieces 1, 2, 4, 8 every total 1 to 15 is a unique combination (binary): e.g. 11 = 8 + 2 + 1.
4. Day plan: day 1 give 1; day 2 take 1 back, give 2; day 3 give 1 again (holds 2 + 1); day 4 swap for 4; and so on.
5. With 2 cuts (3 pieces) only 7 totals exist, so 3 cuts is the minimum.
**Fast method (30 seconds):** Pieces needed = bits needed for 15 = 4, so cuts = 4 - 1 = 3.
**Check:** Checked by brute force: for 0, 1 and 2 cuts no split of 15 works; for 3 cuts the only split that works is {1, 2, 4, 8}.
**Explain simply:**
- Binary means every number is a sum of distinct powers of 2 (1, 2, 4, 8, ...).
- Letting the contractor give pieces back is what allows us to rely on subset sums.
**Likely follow-ups:** A 31-day month with a 31-unit bar? 4 cuts (1, 2, 4, 8, 16). Why not 2 cuts? Three pieces give at most 7 different totals, fewer than the 15 needed.
**Common mistakes / traps:** Giving 15 one-unit pieces (14 cuts), or forgetting the exchange rule, or counting pieces (4) instead of cuts (3).

### Q36 ⭐ 🟡 A worker is paid one link per day for 7 days from a closed chain of 7 links. What is the minimum number of links you must open, and which link do you open?
**Asked at:** commonly asked (no company-specific report found); the gold-chain puzzle is a classic (prep-site claim, unverified).
**What the interviewer is checking:** Whether you use one opened link as a connector that creates pieces of sizes 1, 2 and 4.
**Say this in the interview:** "Open just the third link. It frees a single link and leaves a 2-link piece and a 4-link piece. Those sizes 1, 2, 4 let me make any total 1 to 7 by swapping."
**Answer:** **1 link, the 3rd link from one end (the 5th from the same end works too, by mirror symmetry).**
**Step-by-step reasoning:**
1. Open (and detach) link 3 of the closed chain of 7. The chain falls into: links 1-2 (a piece of 2), link 3 on its own (a piece of 1), links 4-7 (a piece of 4).
2. Day 1: give the single link (1). Day 2: take it back, give the 2-piece. Day 3: give the 2-piece and the single (total 3).
3. Day 4: take both back, give the 4-piece. Day 5: 4 + 1. Day 6: 4 + 2 (take back the single). Day 7: all three, 4 + 2 + 1 = 7.
4. Zero opened links cannot work because you cannot hand over exactly one link from a closed chain.
5. Opening any other link gives piece sizes that cannot make every total from 1 to 7. For example, opening link 4 gives pieces 3, 1, 3, and a total of 2 is impossible.
**Fast method (30 seconds):** You need pieces of size 1, 2, 4 (binary). 1 + 2 + 4 = 7, so the opened link is the one with 2 links on one side and 4 on the other.
**Check:** Checked by script over all 7 choices of the single link to open: only link 3 and link 5 give pieces that can pay every day from 1 to 7; opening 0 links cannot pay one link.
**Explain simply:**
- Opening a link does not destroy it: it turns a closed ring into pieces, and the opened link itself becomes a 1-unit piece.
- The same binary idea as 1-2-4-8 pieces applies.
**Likely follow-ups:** A chain of 15 links? Opening 1 link cannot work, 2 links can (checked by script, for example open links 3 and 7, pieces 2, 3, 8, 1, 1). A 3-link chain? Open the 1st link.
**Common mistakes / traps:** Opening link 4, the middle link (pieces 3, 1, 3), or saying 2 links without testing whether 1 is enough.

### Q37 ⭐ 🟡 Using a two-pan balance with weights placed on either pan, what is the smallest number of weights that can weigh every whole number of kilograms from 1 to 40, and what are they?
**Asked at:** commonly asked (no company-specific report found); the "weights on both pans" puzzle is a classic (prep-site claim, unverified).
**What the interviewer is checking:** Whether you recognise base 3 (each weight can be on the left, on the right or off), not base 2.
**Say this in the interview:** "Each weight has three states, object side, other side or unused, so powers of 3: 1, 3, 9, 27. Four weights reach every whole number up to 40."
**Answer:** **4 weights: 1, 3, 9 and 27 kg.**
**Step-by-step reasoning:**
1. Each weight can go on the pan opposite the object (+), on the same pan as the object (-), or stay off (0): three choices.
2. With k weights you can reach at most (3^k - 1)/2 positive whole numbers. For k = 3 that is 13, so 3 weights cannot reach 40. For k = 4 it is 40, which is exactly enough.
3. So 4 weights is the minimum, and they must use all 81 sign patterns without waste.
4. Powers of 3 do it: 1, 3, 9, 27. Examples: 2 = 3 - 1; 5 = 9 - 3 - 1; 8 = 9 - 1; 20 = 27 - 9 + 3 - 1; 40 = 27 + 9 + 3 + 1.
5. This is the only set: since 4 weights have only exactly 40 positive totals available, any waste breaks coverage.
**Fast method (30 seconds):** Write the number in base 3 with digits -1, 0, 1 ("balanced ternary"); weights are the place values 1, 3, 9, 27. Check 1 + 3 + 9 + 27 = 40, the top of the range.
**Check:** Verified by brute force: of all 91,390 sets of 4 weights from 1 to 40, exactly one covers 1 to 40, namely {1, 3, 9, 27}; no set of 3 weights does.
**Explain simply:**
- A weight on the object's own pan counts as negative.
- Balanced ternary is base 3 with digits -1, 0, +1 instead of 0, 1, 2.
**Likely follow-ups:** Up to 121? 5 weights (1, 3, 9, 27, 81). Weights on one pan only (the earlier question) needs 1, 2, 4, 8, ...: for 40 that is 6 weights.
**Common mistakes / traps:** Using 1, 2, 4, 8, 16, 32 (6 weights) because you forget weights may go on the object's pan.

### Q38 ⭐ 🟡 There are 10 bags with 10 coins each. One bag has all counterfeit coins, each weighing 9 g, while genuine coins weigh 10 g. You have a digital scale and may weigh once. You take 1 coin from bag 1, 2 from bag 2, up to 10 from bag 10 and the scale reads 545 g. Which bag is counterfeit?
**Asked at:** commonly asked (no company-specific report found); the one-weighing counterfeit-bag puzzle is a classic (prep-site claim, unverified). The wording here is a fresh numeric variant.
**What the interviewer is checking:** Whether you design the experiment so that the reading itself names the culprit.
**Say this in the interview:** "If all coins were genuine the scale would read 550 g. It reads 545, which is 5 short. A counterfeit coin is 1 g light, so there are 5 counterfeit coins on the scale, which means bag 5."
**Answer:** **Bag 5 is counterfeit.**
**Step-by-step reasoning:**
1. Coins taken: 1 + 2 + ... + 10 = 55 coins.
2. If all were genuine (10 g each) the scale would read 550 g.
3. Each counterfeit coin weighs 1 g less. If bag b is the counterfeit one, b coins from it are on the scale, so the shortfall is b grams.
4. Shortfall = 550 - 545 = 5, so b = 5.
5. Unique: the shortfall differs for every bag (1 g for bag 1, up to 10 g for bag 10), so each reading points to exactly one bag.
**Fast method (30 seconds):** Reading = 550 - bag number. So bag = 550 - reading.
**Check:** Verified by script: bag b gives reading 550 - b, and 545 occurs only for b = 5.
**Explain simply:**
- Taking a different number of coins from each bag gives each bag a unique "fingerprint" in the total weight.
- This is how one measurement can answer a ten-way question.
**Likely follow-ups:** The reading is 543? Bag 7. What if counterfeit coins weigh 11 g? The reading would be 550 + b, so bag = reading - 550.
**Common mistakes / traps:** Taking the same number of coins from each bag (then the reading cannot tell which bag), or forgetting the shortfall equals the bag number times 1 g.

### Q39 ⭐ 🟡 What is the smallest positive multiple of 7 whose decimal digits are all 0 or 1?
**Asked at:** commonly asked (no company-specific report found); "smallest multiple with only 0/1 digits" is a standard number-sense teaser (prep-site claim, unverified).
**What the interviewer is checking:** Whether you search systematically in increasing order and use a divisibility fact for a shortcut.
**Say this in the interview:** "I list numbers made of 0s and 1s in order and test each for divisibility by 7. The first that works is 1001."
**Answer:** **1001** (= 7 x 143).
**Step-by-step reasoning:**
1. Candidates in increasing order: 1, 10, 11, 100, 101, 110, 111, 1000, 1001, ...
2. Test divisibility by 7 using remainders: 1 gives 1; 10 gives 3; 11 gives 4; 100 gives 2; 101 gives 3; 110 gives 5; 111 gives 6; 1000 gives 6.
3. 1001 divided by 7 is 143 exactly, remainder 0.
4. None of the earlier candidates is a multiple of 7, so 1001 is the smallest.
**Fast method (30 seconds):** 1001 = 7 x 11 x 13 is a famous product, which is why 1001 works. Remember it: it is the base of the "any 3-digit number repeated" trick (e.g. 523523 = 523 x 1001).
**Check:** Checked by brute force over 1 to 10^7: the first 0/1-digit multiple of 7 is 1001, and none exists below 1,001.
**Explain simply:**
- A multiple of 7 leaves remainder 0 when divided by 7.
- Testing in increasing order guarantees the first hit is the smallest.
**Likely follow-ups:** Smallest 0/1-digit multiple of 3? 111 (digit sum 3); of 9? 111111111. Smallest multiple of 11 with only 0 and 1 digits? 11.
**Common mistakes / traps:** Trying only numbers like 1111111 and missing the zeros, or stopping at a number such as 1010 without actually dividing.

### Q40 ⭐ 🟡 You have two ropes, each of which burns for exactly 60 minutes but burns unevenly. How do you measure exactly 90 minutes?
**Asked at:** commonly asked (no company-specific report found); burning-rope puzzles are a classic (prep-site claim, unverified). The classic 45-minute version is avoided on purpose; this variant asks for 90.
**What the interviewer is checking:** Whether you reach for the simplest working plan and still know the "light both ends" trick.
**Say this in the interview:** "Light rope 1 at one end. When it finishes, an hour has passed. At that moment light both ends of rope 2, which burns out in exactly 30 minutes. Total 90 minutes."
**Answer:** **Light rope 1 at one end; when it burns out (60 min) light both ends of rope 2; when it burns out, 90 minutes have passed.**
**Step-by-step reasoning:**
1. Rope 1 lit at one end at time 0 takes exactly 60 minutes to finish (burn speed is uneven but the total is exactly 60).
2. At minute 60, light rope 2 at both ends. Fire travelling from both ends meets when the whole rope is gone; the two flames together consume a full rope's worth of burning in half the time, exactly 30 minutes, whatever the uneven speed.
3. Rope 2 finishes at minute 90.
4. Why both ends gives half: at each instant the two flames burn the rope's "60 minutes of burn time" at a combined rate of 2 per minute, so the total time is 60 / 2 = 30.
**Fast method (30 seconds):** One end = 60 minutes; both ends = 30 minutes; 60 + 30 = 90.
**Check:** Hand-checked on the burn-time argument (no numerical simulation needed; the argument holds for any uneven burn profile).
**Explain simply:**
- The rope is only a clock for "how much burn time is left", not for length. Lighting both ends doubles the rate of using it up.
- Uneven burning does not matter as long as you count total burn time, not burnt length.
**Likely follow-ups:** How do you get 45 minutes? Light rope 1 at both ends and rope 2 at one end; at minute 30 rope 1 is gone; light rope 2's other end; it finishes at minute 45. How do you get 15 minutes? Same set-up, from minute 30 to 45.
**Common mistakes / traps:** Thinking half the rope by length burns in 30 minutes (false for uneven ropes), or concluding that 90 is impossible without the second rope's second end.

### Q41 ⭐ 🟡 You stir a spoonful of milk from glass A (milk) into glass B (water, same volume), mix well, and then return a spoonful of the mixture to glass A. Is there more milk in the water glass or more water in the milk glass?
**Asked at:** commonly asked (no company-specific report found); the milk and water glasses puzzle is a classic (prep-site claim, unverified).
**What the interviewer is checking:** Whether you see a conservation argument rather than doing messy fractions.
**Say this in the interview:** "Both glasses end with the same volume as at the start. Whatever milk is missing from glass A must be replaced by the same volume of water. So the milk in the water glass equals the water in the milk glass."
**Answer:** **They are equal: the amount of milk in glass B equals the amount of water in glass A.**
**Step-by-step reasoning:**
1. Glass A started with only milk and glass B with only water, both with the same volume V. After both transfers, each glass again holds volume V (a spoonful went out, a spoonful came back).
2. Glass A now holds V of liquid, made of milk and water. If it holds m of water, it holds V - m of milk, so m of milk is missing from A.
3. All missing milk must be in glass B, since milk exists only in A and B. So glass B holds exactly m of milk.
4. So water in A = m = milk in B.
5. Spoon size and volume do not matter. Example with V = 100 and a 10-unit spoon: B then holds 110, of which 10/110 is milk; returning 10 brings back 10/11 of milk. Result: milk in B = 100/11 and water in A = 100/11.
**Fast method (30 seconds):** Conservation: "what left A in milk is balanced by what entered A in water, because A's volume is back to normal".
**Check:** Verified with exact fractions for three different glass and spoon sizes (V = 100, 50, 1000; spoons 10, 3, 1): milk in B equals water in A each time (100/11, 150/53, 1000/1001).
**Explain simply:**
- Conservation means a total quantity cannot appear or vanish: glass volumes are unchanged, so swaps must balance.
- Spotting what stays fixed often beats calculating the mixture.
**Likely follow-ups:** What if the spoon is stirred only lightly and not well mixed? The equality still holds as long as the same volume is moved each way. What if you do three round trips? Still equal.
**Common mistakes / traps:** Assuming the milk glass is "purer" because it got a small amount back, or believing the answer depends on how big the spoon is.

### Q42 ⭐ 🟡 You have three containers of capacity 8, 5 and 3 litres. The 8-litre container is full of juice and the others are empty. A move pours from one container into another until the source is empty or the target is full. What is the minimum number of moves to split the juice into 4 litres in the 8-litre container and 4 litres in the 5-litre container?
**Asked at:** commonly asked (no company-specific report found); the 8-5-3 pouring puzzle is a classic (prep-site claim, unverified). The Book 6 jug item is a different 5-3 variant.
**What the interviewer is checking:** Whether you can track a state (amounts in each container) and search for the shortest path.
**Say this in the interview:** "I write the three volumes after each pour and always pour so that something fills or empties. The shortest route takes 7 moves."
**Answer:** **7 moves.**
**Step-by-step reasoning:**
Write (8-litre, 5-litre, 3-litre) after each move:
1. Start: (8, 0, 0).
2. 8 into 5: (3, 5, 0).
3. 5 into 3: (3, 2, 3).
4. 3 into 8: (6, 2, 0).
5. 5 into 3: (6, 0, 2).
6. 8 into 5: (1, 5, 2).
7. 5 into 3: (1, 4, 3).
8. 3 into 8: (4, 4, 0). Goal reached.
9. Moves are counted from step 2 to step 8, which is 7 moves. A search over all reachable states shows that no route with 6 or fewer moves reaches (4, 4, 0), and this 7-move route is the only shortest one.
**Fast method (30 seconds):** Keep pouring the 3-litre into the 8-litre when it is full, and the 5-litre into the 3-litre; this "fill the middle, empty the small" rhythm walks through the states above.
**Check:** Checked by breadth-first search over all (8, 5, 3) states: minimum 7 moves, with exactly one shortest path.
**Explain simply:**
- Each state is just three numbers adding to 8. A move is a pour that stops when the source is empty or the target is full, so there are few options.
- Breadth-first search means trying all 1-move states, then all 2-move states, and so on, so the first time you reach the goal is the shortest.
**Likely follow-ups:** What if the goal were 4 litres in the 5-litre container only, with the rest anywhere? Run the same search from the new goal; a different goal usually has a different shortest path, so check the goal before reusing the moves.
**Common mistakes / traps:** Pouring partly (not allowed by the rules), forgetting that the 3-litre container is also a place to store juice, or counting the starting state as a move.

### Q43 ⭐ 🟡 A digit-counting question: how many times is the digit 7 written when numbering the pages of a 300-page report from 1 to 300?
**Asked at:** commonly asked (no company-specific report found); digit-counting items appear in analytics-firm aptitude rounds as reported by prep sites (unverified).
**What the interviewer is checking:** Whether you count by place value (units, tens, hundreds) instead of writing out 300 numbers.
**Say this in the interview:** "I count the 7s place by place. Units digit: 7, 17, ..., 297 is 30 pages. Tens digit: 70 to 79, 170 to 179, 270 to 279 is 30 pages. No page has a 7 in the hundreds place. So 60."
**Answer:** **The digit 7 is written 60 times.**
**Step-by-step reasoning:**
1. Look at each position separately; a page like 77 counts twice (once per position), which is why we add positions rather than list pages.
2. Units place: a 7 appears once in every block of 10, and 300 pages is 30 blocks: 30 sevens.
3. Tens place: a 7 appears in 70-79 inside every block of 100; there are 3 blocks (1-100, 101-200, 201-300) and each gives 10 pages: 30 sevens.
4. Hundreds place: pages 1-300 only have hundreds digits 0, 1, 2 and 3 (page 300 has hundreds digit 3), so 0 sevens.
5. Total: 30 + 30 + 0 = 60.
**Fast method (30 seconds):** Think of the pages as 000 to 299 (page 300 has no 7, and 000 has none). Every one of the three positions is equally likely to hold any digit, but the hundreds digit only runs 0 to 2, so it never gives a 7. The units and tens positions each hold a 7 in 1 out of 10 numbers: 300 x 2 / 10 = 60.
**Check:** Checked by brute force: counted the character "7" in every number from 1 to 300 (60), also split by position (30 units, 30 tens, 0 hundreds).
**Explain simply:**
- Place value means the digit's position: units (ones), tens, hundreds.
- A given digit shows up in a position once every 10 steps for the units place and 10 out of every 100 for the tens place.
- Counting digit appearances is different from counting pages that contain a 7.
**Likely follow-ups:** 1) *How many 7s are written for pages 1 to 1000?* 3 positions x 100 = 300 (verified by script). 2) *How many 7s from 1 to 100?* 20 (10 in units, 10 in tens), verified by script.
**Common mistakes / traps:** Answering 30 (forgetting the tens place) or counting pages that contain a 7 (page 77 then counts once instead of twice).

### Q44 ⭐ 🟡 How many integers from 1 to 1000 are divisible by none of 2, 3 and 5?
**Asked at:** commonly asked (no company-specific report found); inclusion-exclusion counting is a standard aptitude item.
**What the interviewer is checking:** Whether you can count "none of" by subtracting overlaps correctly (inclusion-exclusion).
**Say this in the interview:** "I count what is divisible by 2, 3 or 5 using inclusion-exclusion: 1000 minus 1033 plus 332 minus 33 equals 266. As a check, every block of 30 numbers has exactly 8 survivors."
**Answer:** **266 integers.**
**Step-by-step reasoning:**
1. Inclusion-exclusion means: add the single sets, subtract the pairs (counted twice), add back the triple (subtracted too often).
2. Singles (round down 1000 divided by the number): by 2: 500; by 3: 333; by 5: 200. Sum 1033.
3. Pairs (divisible by both means by the product): by 6: 166; by 10: 100; by 15: 66. Sum 332.
4. Triple: by 30: 33.
5. Divisible by at least one: 1033 - 332 + 33 = 734. None of them: 1000 - 734 = 266.
**Fast method (30 seconds):** The pattern of divisibility repeats every 30 numbers (30 = 2 x 3 x 5). In each block of 30 the survivors are 1, 7, 11, 13, 17, 19, 23, 29: 8 numbers. 33 full blocks (1 to 990) give 264. Of 991 to 1000 only 991 and 997 survive: 264 + 2 = 266.
**Check:** Checked by brute force over all 1000 integers: 266. The formula and the block method agree.
**Explain simply:**
- "Divisible by none" means not divisible by 2, and not by 3, and not by 5.
- Inclusion-exclusion fixes double counting: a multiple of 6 is in both the "by 2" and the "by 3" lists.
- The repeat-every-30 trick works because the remainders mod 2, 3 and 5 repeat together every 30 steps.
**Likely follow-ups:** 1) *Same question for 1 to 100?* 26 (verified by script). 2) *For 1 to 30?* 8, as in the block list.
**Common mistakes / traps:** Stopping at 1033 and subtracting only that (1000 - 1033 is negative), or forgetting to add back the multiples of 30. Another trap is estimating 1000 x (1/2)(2/3)(4/5) = 266.67 and answering 267; the exact count is 266.

### Q45 ⭐ 🔴 In how many ways can a 2 × 8 strip be tiled completely with 2 × 1 dominoes (each domino can be placed upright or lying down)?
**Asked at:** commonly asked (no company-specific report found); domino tilings are a classic combinatorics puzzle.
**What the interviewer is checking:** Whether you can find a recurrence (a rule that builds the answer from smaller cases) instead of listing arrangements.
**Say this in the interview:** "Look at the last column. Either one upright domino fills it, leaving a 2 by 7 strip, or two lying dominoes fill the last two columns, leaving 2 by 6. So T(n) = T(n-1) + T(n-2), the Fibonacci pattern: 1, 2, 3, 5, 8, 13, 21, 34. Answer 34."
**Answer:** **34 ways.**
**Step-by-step reasoning:**
1. Let T(n) be the number of tilings of a 2 x n strip. A 2 x 1 strip needs one upright domino: T(1) = 1. A 2 x 2 strip takes two upright or two lying: T(2) = 2.
2. Take the rightmost column of a 2 x n strip. It is covered either by an upright domino (the rest is a 2 x (n-1) strip) or by a lying domino on top. A lying domino on top forces a lying domino below it (nothing else fits), so those two cover the last two columns and the rest is 2 x (n-2).
3. These two cases never overlap and cover everything: T(n) = T(n-1) + T(n-2).
4. Table: T(1)=1, T(2)=2, T(3)=3, T(4)=5, T(5)=8, T(6)=13, T(7)=21, T(8)=34.
**Fast method (30 seconds):** Recognise "add the previous two" and write the sequence 1, 2, 3, 5, 8, 13, 21, 34. Count to the 8th term.
**Check:** Checked by brute force: a backtracking program that places dominoes into the first empty cell gave 1, 2, 3, 5, 8, 13, 21, 34 for widths 1 to 8.
**Explain simply:**
- A recurrence builds a big answer from smaller ones; here the last column can only be finished in two ways.
- The Fibonacci sequence is just "each number is the sum of the previous two".
- Two lying dominoes stacked in one place count as one move (they fill two columns together).
**Likely follow-ups:** 1) *A 2 x 10 strip?* 89 (continue the sequence: 34 + 21 = 55, then 89 at width 10; verified by script). 2) *Why can one lying domino not be alone?* It would leave a single empty cell above or below it that no 2 x 1 domino can fill.
**Common mistakes / traps:** Answering 2^8 = 256 or 8, or counting rotations of the whole tiling as extra. Also starting the sequence at 1, 1, 2 and landing on 21 or 55 (an off-by-one).

### Q46 ⭐ 🔴 100 people stand in a circle numbered 1 to 100. Starting with person 1, every second person is eliminated (2, 4, 6, ...) going round and round, and counting continues around the circle among those remaining (so after 100 is removed, 1 is skipped and 3 is next). Which person is the last survivor?
**Asked at:** commonly asked (no company-specific report found); this is the Josephus problem, a classic in programming interviews.
**What the interviewer is checking:** Whether you can find structure (a power of two resets the circle) rather than simulating 100 steps by hand.
**Say this in the interview:** "When the circle size is a power of two, person 1 always survives. 100 is 64 plus 36, so after 36 eliminations there are 64 people left and the next count starts at person 73. So 73 survives."
**Answer:** **Person 73.**
**Step-by-step reasoning:**
1. Start: 100 people, 2 is out, then 4, 6, and so on. Each elimination removes the next-but-one person.
2. Key fact: with a power of two people (2, 4, 8, 16, 32, 64), the first person to be counted always survives. Why: one full lap removes exactly half the people and leaves the first person to be counted again, still first, in a circle half the size; repeat until one is left.
3. 100 - 36 = 64, a power of two. So aim to reach 64 people.
4. The first 36 eliminations remove persons 2, 4, 6, ..., 72 (the 36th even number is 72). Now 64 people remain: 1, 3, 5, ..., 71, and 73 to 100.
5. The count restarts at the next person after 72, which is 73. By the key fact, 73 survives.
**Formula:** Write the number of people as n = 2^m + L (here 100 = 64 + 36). The survivor is 2L + 1 = 73.
**Fast method (30 seconds):** n = 100: biggest power of two not above it is 64, L = 36, answer 2 x 36 + 1 = 73.
**Check:** Checked by simulation of the circle: the last survivor is 73, and the first eliminated are 2, 4, 6, 8, 10 as the question says.
**Explain simply:**
- "Josephus problem" means eliminating every k-th person in a circle; here k = 2.
- Powers of two work nicely because every lap removes exactly half.
- The formula 2L + 1 just says "the first person to be counted after L eliminations is person 2L + 1".
**Likely follow-ups:** 1) *64 people?* Person 1 (L = 0), verified by script. 2) *1000 people?* 1000 = 512 + 488, answer 977 (verified by script).
**Common mistakes / traps:** Answering 1 or 100 by guessing, or 99 by forgetting that counting continues round and round. Also an off-by-one: starting the next count at 72 rather than 73.

### Q47 ⭐ 🔴 A 4 × 4 × 4 cube must be cut into 64 unit cubes. If you may rearrange (stack) the pieces between cuts, what is the minimum number of straight cuts needed, and what is the plan?
**Asked at:** commonly asked (no company-specific report found); a standard "can you use rearrangement" puzzle.
**What the interviewer is checking:** Whether you see that stacking lets every cut work on many pieces at once, which turns 9 cuts into 6 by halving.
**Say this in the interview:** "Each direction needs the cube cut into 4 equal strips. Cut in half, stack the halves, cut in half again: 2 cuts. Do that for length, width and height: 6 cuts. Fewer is not possible because one cut can at most double the number of pieces along a direction, and 4 needs two doublings."
**Answer:** **6 cuts.**
**Plan:**
1. Cut 1: cut the 4 x 4 x 4 cube at the middle in the x direction into two 2 x 4 x 4 slabs.
2. Cut 2: stack the two slabs on top of each other (aligned) and cut through both at the middle: four 1 x 4 x 4 slabs.
3. Cuts 3 and 4: arrange the four slabs so they form a block, and cut in the y direction the same way (middle, restack, middle): sixteen 1 x 1 x 4 sticks.
4. Cuts 5 and 6: line up the sixteen sticks, cut at the middle, restack, cut again: 64 unit cubes.
**Step-by-step reasoning (why 6 is the minimum):**
1. A cut is a flat slice. To get unit cubes you must separate every pair of neighbouring cells along each of the three directions. Along one direction there are 3 internal boundaries (after length 1, 2 and 3).
2. With stacking, k cuts in one direction can handle at most 2^k - 1 boundaries (each cut can at best double the number of pieces along that line: 1, 2, 4, ...). Three boundaries need 2^k - 1 at least 3, so k is at least 2.
3. A cut slices along one direction only, so the three directions cannot share cuts: at least 2 + 2 + 2 = 6.
4. The plan above uses exactly 6, so 6 is the minimum.
**Fast method (30 seconds):** Per direction: ceil(log2 of side) = log2 4 = 2 cuts. Three directions: 6. Without stacking you would need 3 cuts per direction, 9 in total.
**Check:** The one-direction part was verified by a breadth-first search over stacked piece lengths (a length-4 stick needs exactly 2 cuts; 2 needs 1; 3 needs 2; 5 needs 3). The "directions cannot share cuts" step is a hand argument, assuming flat cuts parallel to the faces.
**Explain simply:**
- "Stacking" means you move pieces on top of each other between cuts so one saw pass cuts several.
- Each pass at best doubles the number of pieces in a line: 1, 2, 4. That is why the count is a logarithm.
- Cuts in different directions do different jobs, so you add them.
**Likely follow-ups:** 1) *A 5 x 5 x 5 cube?* ceil(log2 5) = 3 per direction, so 9 (the 1-D part verified by script). 2) *A 3 x 3 x 3 cube with stacking?* 2 per direction, so 6.
**Common mistakes / traps:** Answering 9 (3 cuts per direction, the no-stacking answer) or 3 (one cut per direction). Also assuming that diagonal cuts could do better; they do not help separate the grid cells.

### Q48 ⭐ 🔴 There are 10 bottles, each filled with 10 g pills. Some bottles (possibly several, possibly none) contain defective pills that each weigh 9 g. Using a digital scale only once, how do you find which bottles are defective, and which bottles are defective if you take 2^(i-1) pills from bottle i (i = 1 to 10) and the scale reads 10,205 g?
**Asked at:** commonly asked (no company-specific report found); the counterfeit-coins-in-bags idea is a classic scale puzzle (here as a pill variant with binary weights).
**What the interviewer is checking:** Whether you can encode information in counts so that one reading identifies a whole set (binary encoding).
**Say this in the interview:** "Take 1 pill from bottle 1, 2 from bottle 2, 4 from bottle 3, then double each time, so 2^(i-1) from bottle i. If every pill weighed 10 g the total would be 1023 pills = 10,230 g. Each defective bottle takes away as many grams as pills I took from it. The shortfall, 25, is 1 + 8 + 16, so bottles 1, 4 and 5 are defective."
**Answer:** **Bottles 1, 4 and 5 are defective** (shortfall 10,230 - 10,205 = 25 g = 1 + 8 + 16).
**Step-by-step reasoning:**
1. Total pills taken: 1 + 2 + 4 + ... + 512 = 1023, so the expected weight with no defects is 10,230 g.
2. A defective pill is 1 g light. If bottle i is defective, you took 2^(i-1) of its pills and the total is 2^(i-1) g lighter.
3. So shortfall = the sum of 2^(i-1) over the defective bottles. This is a binary number: bit i is 1 exactly when bottle i is defective.
4. Shortfall 25 = 16 + 8 + 1 = 11001 in binary. Reading the bits from the right: bottle 1 = 1, bottle 2 = 0, bottle 3 = 0, bottle 4 = 1, bottle 5 = 1, bottles 6 to 10 = 0.
5. Defective bottles: 1, 4 and 5. Check the pills: 1 + 8 + 16 = 25 light pills, 10,230 - 25 = 10,205 g.
**Fast method (30 seconds):** Convert the shortfall into binary by subtracting the biggest power of two each time: 25 - 16 = 9, 9 - 8 = 1, 1 - 1 = 0. Powers used: 16 (bottle 5), 8 (bottle 4), 1 (bottle 1). It is unique because every whole number has only one binary form.
**Check:** Checked by brute force over all 1024 possible defect sets: all 1024 shortfalls are different (so any reading identifies the set uniquely), and the only set giving 10,205 g is {1, 4, 5}.
**Explain simply:**
- Binary is counting with powers of two (1, 2, 4, 8, ...); every number is a unique sum of them.
- Taking 2^(i-1) pills gives each bottle its own "fingerprint" amount that cannot be confused with any combination of others.
- This works for any number of defective bottles, not just one, which is why it is more powerful than the one-bad-bag version.
**Likely follow-ups:** 1) *Reading 10,226 g?* Shortfall 4 = 100 in binary, so only bottle 3 (verified by script). 2) *Why not take 1, 2, 3, 4, ... pills?* Then different sets can give the same shortfall (for example bottles 1 and 2 vs bottle 3 both give 3).
**Common mistakes / traps:** Taking the same number of pills from each bottle (you cannot tell which one is light), or treating the puzzle as having only one defective bottle.

### Q49 ⭐ 🔴 What is the largest number of identical-looking balls, exactly one of which has a different weight (heavier or lighter, unknown), among which you can always find the odd ball in 3 weighings on a balance (you need not say whether it is heavier or lighter)?
**Asked at:** commonly asked (no company-specific report found); the 12-balls puzzle is a famous brain teaser. This version asks for the largest number of balls and does not require telling heavier from lighter.
**What the interviewer is checking:** Whether you can reason about outcomes: each weighing has 3 results (left heavier, right heavier, equal), so k weighings give 3^k results.
**Say this in the interview:** "Three weighings give 27 outcomes. If I only need to find the ball and not say whether it is heavy or light, the maximum is (3^3 - 1) / 2 = 13 balls. I would weigh 4 against 4 first."
**Answer:** **13 balls.**
**Step-by-step reasoning:**
1. Counting bound: each ball could be heavy or light, so N balls give 2N scenarios. A ball that is never on the scale produces "all balanced" and needs just one outcome; every other ball needs two different outcomes. That gives 2(N - 1) + 1 at most 27, so N is at most 14 by counting alone.
2. The real limit is tighter, because the first weighing must have equal numbers of balls on each side (there is no known genuine ball yet). An exhaustive search over all possible weighings (a dynamic programme over "how many balls are still suspects, and of which kind") shows 13 balls can always be solved in 3 weighings and 14 cannot.
3. Plan for balls 1 to 13. **Weighing 1:** 1-4 against 5-8.
4. **If equal:** the odd ball is among 9 to 13 and balls 1 to 8 are genuine. Weighing 2: 9, 10, 11 against 1, 2, 3. If they differ, the odd one is among 9-11 and you know whether it is heavy or light from the tilt; weighing 3: 9 against 10; the one that matches the known direction is odd, and if equal it is 11. If weighing 2 is equal, the odd ball is 12 or 13; weighing 3: 12 against a genuine ball; if they differ it is 12, if equal it is 13.
5. **If 1-4 are heavier than 5-8:** balls 1-4 may be heavy, 5-8 may be light, 9-13 are genuine. Weighing 2: {1, 2, 5} against {3, 6, 9}. Left side heavier means 1 or 2 is heavy or 6 is light: weighing 3: 1 against 2 (heavier is odd, equal means 6). Right side heavier means 3 is heavy or 5 is light: weighing 3: 3 against a genuine ball (if it is heavier it is 3, else 5). Equal means 4 is heavy or 7 or 8 is light: weighing 3: 7 against 8 (lighter is odd, equal means 4). The mirror case (5-8 heavier) swaps the roles.
**Fast method (30 seconds):** The formula for finding the ball only is (3^k - 1) / 2: 1, 4, 13, 40 for k = 1 to 4. (If you also must say heavy or light, the maximum drops to (3^k - 3) / 2, which is 12 for k = 3; that second formula is from memory and was not run here.)
**Check:** Verified by script: the full plan above was simulated for all 26 cases (each of 13 balls heavy or light) and always names the right ball; the search confirmed 13 solvable and 14 not for k = 3 (and 4 solvable, 5 not for k = 2; 40 solvable, 41 not for k = 4).
**Explain simply:**
- A balance has three outcomes, not two, so each weighing can split the suspects into three groups.
- Balls that were on the scale in a balanced weighing become "known genuine" and can be used as reference weights later.
- Not needing to know heavy or light saves one extra ball compared with the full version.
**Likely follow-ups:** 1) *Four weighings?* 40 balls (verified by script). 2) *If one genuine ball is given as a spare from the start?* The first weighing can then be unequal, and the counting bound is reachable: 14 balls for 3 weighings, and 15 is impossible (verified by the same search).
**Common mistakes / traps:** Answering 27 (forgetting that each ball can be heavy or light) or 12 (the classic version in which you must also report heavy or light). Also weighing 6 against 6 first: after a tilt, 12 suspects remain and only 2 weighings are left (at most 9 outcomes).

### Q50 ⭐ 🔴 What is the minimum number of pairwise comparisons that guarantees finding both the largest and the smallest of 8 distinct numbers, and how do you do it?
**Asked at:** commonly asked (no company-specific report found); "max and min together" is a standard algorithm-flavoured puzzle.
**What the interviewer is checking:** Whether you avoid the wasteful approach (7 + 6 = 13) by sharing comparisons between the two jobs.
**Say this in the interview:** "Pair the 8 numbers up: 4 comparisons. The 4 winners contain the maximum, the 4 losers contain the minimum. Maximum of 4 winners takes 3 comparisons, minimum of 4 losers takes 3. Total 4 + 3 + 3 = 10."
**Answer:** **10 comparisons.**
**Step-by-step reasoning:**
1. Split the numbers into 4 pairs and compare within each pair: 4 comparisons. Now every pair has a winner (larger) and a loser (smaller).
2. The overall largest must have won its own pair (the number it met was smaller), so it is among the 4 winners. Likewise the overall smallest is among the 4 losers.
3. Largest of the 4 winners: 3 comparisons (a knockout: 2 + 1).
4. Smallest of the 4 losers: 3 comparisons.
5. Total 4 + 3 + 3 = 10. The general rule is ceil(3n / 2) - 2, which is 10 for n = 8.
**Fast method (30 seconds):** For even n: n/2 pair comparisons, then (n/2 - 1) for the max and (n/2 - 1) for the min: n/2 + 2(n/2 - 1) = 3n/2 - 2 = 10. Compare with the naive method (find the max in 7, then the min of the other 7 in 6, total 13).
**Check:** Verified by script: the method was run on all 40,320 orderings of 8 distinct numbers, always using exactly 10 comparisons and always returning the correct max and min. That 10 cannot be beaten was verified by exhaustive search (an adversary game over all comparison outcomes) for n = 2 to 6, giving 1, 3, 4, 6, 7, exactly the formula; for n = 8 the lower bound of 10 is the known general result, not searched directly here.
**Explain simply:**
- Each comparison should teach you two things at once: "this one cannot be the maximum" and "that one cannot be the minimum".
- A pair comparison does exactly that, which is why the pairing step is efficient.
- "Distinct" matters: with ties the problem needs more care.
**Likely follow-ups:** 1) *Six numbers?* ceil(18 / 2) - 2 = 7 (verified by script search). 2) *Why can't you do better?* Every number must lose at least once (except the max) and win at least once (except the min); the counting gives 3n/2 - 2.
**Common mistakes / traps:** Answering 13 or 12 (two separate searches), or 7 (only the max). Also forgetting that the max comes from the winners only, not from all 8.

### Q51 ⭐ 🔴 What is the minimum number of pairwise comparisons that guarantees finding the second-largest of 8 distinct numbers, and how do you organise them?
**Asked at:** commonly asked (no company-specific report found); this is the "runner-up in a tournament" puzzle, which tests whether you reuse earlier comparisons.
**What the interviewer is checking:** Whether you see that the second-largest must have lost directly to the champion, so only a few candidates remain.
**Say this in the interview:** "Run a knockout tournament: 4, then 2, then 1 matches, 7 comparisons. The champion played 3 matches, so the second-largest is one of the 3 players the champion beat directly. Find the largest of those 3 with 2 more comparisons. Total 9."
**Answer:** **9 comparisons.**
**Step-by-step reasoning:**
1. Knockout: 4 comparisons in round 1 (8 numbers become 4 winners), 2 in round 2, 1 in the final: 7 comparisons find the largest.
2. The second-largest number lost only to the largest one (anyone else it met was smaller). So it lost directly to the champion in some round.
3. The champion played 3 matches (8 players: 3 rounds), so it has beaten exactly 3 players directly.
4. The second-largest is the biggest of those 3. Finding the max of 3 takes 2 comparisons.
5. Total 7 + 2 = 9. The general rule is n + ceil(log2 n) - 2 = 8 + 3 - 2 = 9.
**Fast method (30 seconds):** Draw the knockout bracket, circle the champion's three opponents (one per round), compare them. The answer is n - 1 + (log2 n - 1) = 7 + 2.
**Check:** Verified by script: the bracket method was run on all 40,320 orderings of 8 distinct numbers; it always used exactly 9 comparisons and returned the true second-largest. The minimum was confirmed by exhaustive search for n = 2 to 5 (1, 3, 4, 6, matching the formula); for n = 8 the lower bound of 9 is the known result, not searched directly here.
**Explain simply:**
- A knockout bracket is a record of who lost to whom.
- The runner-up is not necessarily the loser of the final. The true second-best might have met the champion earlier in the bracket.
- Reusing earlier results is the saving: a fresh search for the second-largest after finding the max would cost 6 more.
**Likely follow-ups:** 1) *16 numbers?* 16 + 4 - 2 = 18. 2) *Why not just compare the final's loser?* The second-best may have been knocked out by the champion in round 1 or 2.
**Common mistakes / traps:** Answering 13 (7 for the max, then 6 more among the remaining 7) or 8 (assuming the final's loser is second). The correct count needs the champion's opponents, not only the finalists.

### Q52 ⭐ 🔴 Five people need 1, 3, 6, 8 and 12 minutes to cross a bridge at night with one torch. At most two cross at a time at the slower person's pace, and the torch must be carried back for each return trip. What is the minimum total time for all five to cross?
**Asked at:** commonly asked (no company-specific report found); the bridge-and-torch puzzle is a classic, and this is a five-person variant.
**What the interviewer is checking:** Whether you test the two shuttle strategies and notice that the two slowest should cross together.
**Say this in the interview:** "The two slowest, 8 and 12, should cross together so their times are paid once. I use the fast pair, 1 and 3, as torch carriers. Schedule: 1 and 3 cross (3), 1 returns (1), 8 and 12 cross (12), 3 returns (3), 1 and 6 cross (6), 1 returns (1), 1 and 3 cross (3). Total 29 minutes."
**Answer:** **29 minutes.**
**Step-by-step reasoning:**
1. A pair crosses at the slower person's speed, so pairing the two slowest (8 and 12) costs only 12 instead of 8 + 12 = 20.
2. To move the two slowest, compare two ways with the fastest (1) and the second-fastest (3): (a) escort one at a time with 1: 12 + 1 + 8 + 1 = 22 minutes, or (b) send 1 and 3 over, 1 back, 8 and 12 across, 3 back: 3 + 1 + 12 + 3 = 19 minutes. Option (b) is better here.
3. After option (b), the left bank holds 1, 3 and 6 with the torch back on the left (3 returned it). Three people take at best 3 + 1 + 6 = 10 minutes (1 and 3 cross, 1 returns, 1 and 6 cross), or 6 + 1 + 3 = 10 the other way.
4. Total 19 + 10 = 29.
```
Move                      Time   Left bank          Right bank
1,3 cross                  3     6, 8, 12           1, 3
1 returns                  1     1, 6, 8, 12        3
8,12 cross                12     1, 6               3, 8, 12
3 returns                  3     1, 3, 6            8, 12
1,6 cross                  6     3                  1, 6, 8, 12
1 returns                  1     1, 3               6, 8, 12
1,3 cross                  3     (none)             all five
Total                     29
```
**Fast method (30 seconds):** Repeat this rule while four or more people remain on the starting side: move the two slowest across using the cheaper of two options: 2nd + 1st + slowest + 2nd, or slowest + 1st + 2nd-slowest + 1st. Finish the last three with 2nd + 1st + slowest.
**Check:** Verified by script: a shortest-path search over every possible state (who is on which bank, where the torch is) gives 29 as the minimum, and finds 8 different ways to reach it. The naive "1 escorts everyone" plan takes 32.
**Explain simply:**
- Every return trip costs time too, so the person who returns should be fast.
- Slow people should never cross alone and should be paired with the other slow one.
- Greedy "fastest always escorts" is not always best; you compare strategies.
**Likely follow-ups:** 1) *Times 1, 2, 5, 10?* 17 (verified by script). 2) *Times 1, 2, 3, 4, 5?* 16 (verified by script).
**Common mistakes / traps:** Answering 32 (the fastest person escorts everyone) or 3 + 1 + 6 + 1 + 8 + 1 + 12 style totals. Another error is forgetting that the torch must come back after each crossing except the last.

### Q53 ⭐ 🔴 In the cryptarithm EAT + THAT = APPLE, every letter stands for a different digit and no number starts with 0. What is the value of APPLE?
**Asked at:** commonly asked (no company-specific report found); cryptarithms are a standard logical-reasoning staple.
**What the interviewer is checking:** Whether you solve by the carries and size limits column by column instead of trying digits at random.
**Say this in the interview:** "A 3-digit number plus a 4-digit number is at most 10,998, so APPLE starts with 1 and its second digit is 0: A = 1, P = 0. For the sum to reach 10,000, T must be 9. Then 9 + 9 = 18 gives E = 8 with a carry, which fixes L = 3 and H = 2. EAT = 819, THAT = 9219, APPLE = 10038."
**Answer:** **APPLE = 10038** (819 + 9219 = 10038).
**Step-by-step reasoning:**
1. Size: EAT is at most 999 and THAT at most 9999, so the sum is at most 10,998. APPLE has 5 digits, so A = 1 and the next digit P is 0 (10,998 is the ceiling). Then P = 0 in both places.
2. The sum must be at least 10,000. If T were 8 or less, THAT is at most 8999 and EAT is at most 999, so the sum is at most 9998, below 10,000. So T = 9.
3. Units column: T + T = 9 + 9 = 18, so E = 8, carry 1.
4. Tens column: A + A + carry 1 = 1 + 1 + 1 = 3, so L = 3, no carry.
5. Hundreds column: E + H = 8 + H must end in P = 0 and produce a carry into the thousands: H = 2 (8 + 2 = 10).
6. Thousands column: T + carry 1 = 9 + 1 = 10: gives digit 0 = P and carry 1 = A. Consistent.
7. Digits used: E = 8, A = 1, T = 9, H = 2, P = 0, L = 3, all different.
```
   E A T      8 1 9
 T H A T    9 2 1 9
 -------   --------
 A P P L E 1 0 0 3 8
```
**Fast method (30 seconds):** Use size first (the answer is 5 digits from a 3-digit plus a 4-digit number, so it begins 10...), then work from the units column leftwards with carries.
**Check:** Verified by brute force over all assignments of different digits to the six letters (with no leading zeros): exactly one solution, 819 + 9219 = 10038.
**Explain simply:**
- A cryptarithm replaces digits by letters; the same letter is always the same digit, different letters are different digits.
- A "carry" is the 1 you carry to the next column when a column sums to 10 or more.
- Bounding the size of the answer often fixes the first digits at once.
**Likely follow-ups:** 1) *Why must P be 0?* The sum is under 11,000, so its thousands digit (P) is 0 or 1; it cannot be 1 because A is already 1 and different letters need different digits. 2) *Is the solution unique?* Yes, one assignment only (brute force).
**Common mistakes / traps:** Forgetting that P is the same letter in two places (it is 0 in both), or dropping the carries. Trying T = 8 fails because the sum cannot reach 10,000.

### Q54 ⭐ 🔴 The product of the ages of three children is 72. A mathematician is told the sum of their ages and still cannot determine the ages. He is then told that there is a unique eldest child, and he works out the ages. What are the ages?
**Asked at:** commonly asked (no company-specific report found); this is the classic "ages of the children" puzzle with a changed product.
**What the interviewer is checking:** Whether you can use a clue about what the listener could not conclude, then a second clue that breaks the tie.
**Say this in the interview:** "List all age triples with product 72 and their sums. Only one sum, 14, appears twice: 2, 6, 6 and 3, 3, 8. The mathematician needed the extra clue, so the sum must be 14. 'A unique eldest' rules out 2, 6, 6 (two children tied for eldest), so the ages are 3, 3 and 8."
**Answer:** **The children are 3, 3 and 8 years old.**
**Step-by-step reasoning:**
1. List every whole-number triple with product 72 (youngest first) and its sum:
```
(1,1,72)=74   (1,2,36)=39   (1,3,24)=28   (1,4,18)=23
(1,6,12)=19   (1,8,9)=18    (2,2,18)=22   (2,3,12)=17
(2,4,9)=15    (2,6,6)=14    (3,3,8)=14    (3,4,6)=13
```
2. If the sum were any value other than 14, the mathematician would know the answer at once. He "still cannot determine" it, so the sum is 14, which appears twice: (2, 6, 6) and (3, 3, 8).
3. "There is a unique eldest child": in (2, 6, 6) the two oldest are both 6, so there is no single eldest. In (3, 3, 8) the oldest, 8, stands alone.
4. So the ages are 3, 3 and 8. It is unique because step 2 left exactly two candidates and step 3 eliminates one.
**Fast method (30 seconds):** Write the 12 triples and sums, spot the one repeated sum (14), and use the "eldest" clue as the tie-breaker. The twins (3, 3) are fine; only the tied-for-eldest triple is rejected.
**Check:** Verified by script: the enumeration of triples with product 72 gives exactly these 12, only the sum 14 repeats, and applying the unique-eldest rule leaves only (3, 3, 8).
**Explain simply:**
- The puzzle uses knowledge about knowledge: "he cannot tell" is information in itself.
- "Unique eldest" means strictly older than the others, so twins are allowed among the younger ones but not at the top.
- Every statement in a puzzle like this should be used exactly once.
**Likely follow-ups:** 1) *Product 36 with the same two clues?* The only repeated sum is 13 ((1, 6, 6) and (2, 2, 9)); the unique-eldest clue picks 2, 2, 9 (verified by script). 2) *What if the second clue were removed?* Two answers (2, 6, 6 and 3, 3, 8) remain, so the puzzle would be ambiguous.
**Common mistakes / traps:** Picking (2, 6, 6) because the numbers look nice, or thinking the eldest clue means the ages are all different (twins are allowed among the younger ones). Also forgetting that ages (1, 1, 72) are mathematically allowed even if silly.

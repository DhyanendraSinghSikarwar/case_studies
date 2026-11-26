# Book 13 — Logical Reasoning & Analytical Thinking | Part 11: Timed Mixed Mock Sets 🟡🔴

**Target:** 40 questions | **Actual:** 40 questions
**Scope:** Timed mixed mock sets in online-assessment style, four sets of 10 new questions each that mix the topics of Parts 2-10 (syllogisms, inequalities, ranking, blood relations, coding, directions, seating, grids, schedules, truth-tellers, SQL/Excel logic, pseudocode tracing, critical reasoning, counting, weighing). Questions are sorted by mock set (set order, then question order inside the set), not by stars. Set strategies (the minutes and strategies are our suggestion, not an official test format; the minutes are the sum of the suggested times in the question headings): Set 1: Mock Set 1 (warm-up, 10 questions, about 13 minutes; strategy: bank the quick marks first, skip any item that has no clear start after 20 seconds, and note which skipped items you would solve with five more minutes) | Set 2: Mock Set 2 (conditional logic and puzzles, 10 questions, about 15 minutes; strategy: do the one-line logic items and the trace items first, and leave the arrangement puzzles for the last third) | Set 3: Mock Set 3 (harder mixed set, 10 questions, about 17 minutes; strategy: expect two items you should skip, attempt grid and schedule puzzles only after the quick items, and keep a two-minute rule per puzzle) | Set 4: Mock Set 4 (full simulation, 10 questions, about 14 minutes; strategy: treat it as the real test, no pauses, mark for review instead of lingering, then score it with the review method of Part 1)

### Q1 ⭐⭐⭐ 🟢 Mock Set 1, Q1 (suggested time 75 seconds): Statements: All payroll files are encrypted. Some encrypted files are archived. No archived file is public. Conclusions: I. Some payroll files are archived. II. Some archived files are encrypted. III. Some encrypted files are not public. Which conclusions follow, and why does the other one not follow?
**Asked at:** commonly asked (no company-specific report found); syllogisms are listed among Mu Sigma logical-reasoning topics in prep-site summaries (reported, unverified).
**Target time:** 75 seconds (as in the heading).
**What the interviewer is checking:** Whether you can tell what is guaranteed from what is merely possible, using the rule that every named group exists and "some" means at least one.
**Say this in the interview:** "II is just the second statement turned around. III follows because an archived-and-encrypted file exists and archived files are not public. I does not follow: the encrypted files that are archived may sit outside payroll."
**Answer:** **Conclusions II and III follow. Conclusion I does not follow.**
**Step-by-step reasoning:**
1. Convention: every group named (payroll, encrypted, archived, public) has at least one member; "some" means at least one.
2. II: "Some encrypted files are archived" reads the same as "Some archived files are encrypted" (a "some" statement can be flipped). Follows.
3. III: pick one encrypted file that is archived (statement 2 says one exists). No archived file is public, so that file is not public. So some encrypted file is not public. Follows.
4. I: payroll files sit inside encrypted files, but statement 2 never says the archived ones are the payroll ones. Draw payroll as a small circle inside the encrypted circle, and the archived circle can overlap encrypted outside payroll. Then no payroll file is archived. So I is possible but not forced.
**Fast method (30 seconds):** Test each conclusion by trying to break it with a picture. Try to draw a diagram where the conclusion is false; if you can, it does not follow. For I, the diagram "archived overlaps encrypted, away from payroll" breaks it in five seconds.
**Check:** Checked by brute force: I listed every way to fill the 16 possible file types (payroll, encrypted, archived, public yes/no), kept those obeying the statements, and tested 312 models. II and III held in all 312; I failed in 88 of them.
**Explain simply:**
- "All A are B" puts A fully inside B. It does not say B is all A.
- "Some" only guarantees one member in the overlap; it does not say which other groups that member belongs to.
- A conclusion "follows" only if it is true in every possible picture, not just one.
**Likely follow-ups:** 1) *Does "Some payroll files are encrypted" follow?* Yes: payroll is non-empty and all of it is encrypted. 2) *Would I follow if statement 2 were "Some payroll files are archived"?* Then yes, directly.
**Common mistakes / traps:** Chaining "All payroll are encrypted" with "Some encrypted are archived" into "Some payroll are archived" (the middle term is only partly covered); stopping after finding one picture where a conclusion is true.
**If you are short of time (our suggestion):** Do not skip; bank II and III (they follow directly from the statements) and mark I as not following if you cannot draw it in 20 seconds.

### Q2 ⭐⭐⭐ 🟢 Mock Set 1, Q2 (suggested time 60 seconds): Statement: M > N = O >= P < Q. Conclusions: I. M > P. II. N >= P. III. Q > N. Which conclusions definitely follow?
**Asked at:** commonly asked (no company-specific report found); inequality-chain items are a standard bank and IT-service aptitude topic (prep-site claim, unverified).
**Target time:** 60 seconds (as in the heading).
**What the interviewer is checking:** Whether you read a chain left to right and only draw conclusions the chain forces.
**Say this in the interview:** "I follow the chain M, N, O, P and combine the signs. M is above N, N equals O, O is at least P, so M is strictly above P. N is at least P too. Q is only linked to P, not to N, so I cannot compare Q with N."
**Answer:** **Conclusions I and II follow. III does not.**
**Step-by-step reasoning:**
1. Chain: M > N = O >= P < Q. Read it as a ladder.
2. I (M > P): M > N, N = O, O >= P. A strict step plus equal and "at least" steps gives strictly greater. Follows.
3. II (N >= P): N = O and O >= P, so N >= P. Follows.
4. III (Q > N): the only link to Q is P < Q. P is below both N (or equal) and Q, so N and Q are both on the high side of P with nothing connecting them. Not forced.
**Fast method (30 seconds):** Two items are comparable only if one path of signs joins them going the same direction (all "greater" or "greater-or-equal"). The sign meeting at P is "<" from Q and "<=" from O/N, so both point down to P; two arrows into the same point say nothing about each other. Rule of thumb: a combined sign is strict if at least one step is strict.
**Check:** Checked by brute force over all 7,776 value assignments of 0 to 5; 140 satisfy the chain. I and II held in all 140; III held in 105, so it is not forced.
**Explain simply:**
- ">" is strictly greater; ">=" is greater or equal; "=" is equal.
- Combining signs: strict plus anything in the same direction is strict; only ">=" with "=" or ">=" stays "or equal".
- "Definitely follows" means true for every set of numbers that fits the chain.
**Likely follow-ups:** 1) *Does Q > P follow?* Yes, it is written directly (also 140 of 140 cases). 2) *Does M > Q follow?* No: only 70 of 140 cases, so it is not forced.
**Common mistakes / traps:** Treating the "<" at the end as if Q were also below M; reading ">=" as strictly greater and then wrongly accepting an "or equal" conclusion stated as strict.
**If you are short of time (our suggestion):** Do not skip; answer from the chain, and reject any conclusion that compares Q with M or N.

### Q3 ⭐⭐⭐ 🟢 Mock Set 1, Q3 (suggested time 75 seconds): In a hiring test with 45 candidates and no ties in rank, Dev is 14th from the top and Eva scored lower than Dev with exactly 7 candidates ranked between them. What is Eva's rank from the bottom?
**Asked at:** commonly asked (no company-specific report found); ranking items are a standard reasoning-gate topic (prep-site claim, unverified).
**Target time:** 75 seconds (as in the heading).
**What the interviewer is checking:** Whether you handle "from the top / from the bottom" counting, including the off-by-one at the person's own position.
**Say this in the interview:** "Eva is lower than Dev with 7 between them, so she is 14 plus 7 plus 1, which is 22nd from the top. From the bottom it is 45 minus 22 plus 1, so 24th."
**Answer:** **24th from the bottom.**
**Step-by-step reasoning:**
1. Dev is 14th from the top. Eva is below him, so her rank number is bigger.
2. Seven people sit between them: ranks 15 to 21. Eva is the next one, rank 22 from the top.
3. Rank from bottom = total minus rank from top plus 1 = 45 - 22 + 1 = 24.
**Fast method (30 seconds):** Rank from top plus rank from bottom always equals total plus 1 (here 46). So 46 - 22 = 24. Why: the person counts once from each side, so the two counts overlap on themselves.
**Check:** Checked by script: 14 + 7 + 1 = 22, and 22 + 24 = 46 = 45 + 1.
**Explain simply:**
- "7 between" means 7 people strictly between, so the gap is 8 ranks, not 7.
- "No ties" means every rank number is used exactly once.
- Top and bottom ranks add up to total + 1.
**Likely follow-ups:** 1) *If Eva were higher than Dev with 7 between?* Eva is 14 - 8 = 6th from the top, 40th from the bottom (script-checked). 2) *Same data, but 9 between and Eva lower?* 14 + 10 = 24th from top, 22nd from bottom (script-checked).
**Common mistakes / traps:** Answering 21 or 22 from the bottom by forgetting the +1; adding 7 only and landing on 21 from the top.
**If you are short of time (our suggestion):** Do not skip; this is a one-line sum worth full marks. Skip only after the 75 seconds are gone.

### Q4 ⭐⭐⭐ 🟢 Mock Set 1, Q4 (suggested time 75 seconds): Naveen's mother's only brother has a daughter, and she is Tara's mother. How is Naveen related to Tara?
Options: (a) maternal uncle (b) mother's cousin (c) cousin (d) nephew
**Asked at:** commonly asked (no company-specific report found); blood-relation items are a standard aptitude topic (prep-site claim, unverified).
**Target time:** 75 seconds (as in the heading).
**What the interviewer is checking:** Whether you can follow a family chain one link at a time and name the final relation correctly, including the direction.
**Say this in the interview:** "Naveen's mother's only brother is Naveen's maternal uncle. His daughter is Naveen's cousin. She is Tara's mother. So Naveen is Tara's mother's cousin, option (b)."
**Answer:** **(b) Naveen is Tara's mother's cousin.** Reading used: "How is Naveen related to Tara?" asks what Naveen is to Tara, so option (b) means "Naveen is the cousin of Tara's mother". The opposite reading (what Tara is to Naveen) would give "Naveen's cousin's child", which is not among the options, so the options only fit our reading.
**Step-by-step reasoning:**
1. Naveen's mother's brother = Naveen's maternal uncle (mama).
2. The uncle's daughter = Naveen's cousin (a child of your parent's sibling).
3. That cousin is Tara's mother. So Tara is the cousin's child (Tara's gender is not given).
4. Naveen is the cousin of Tara's mother. So Naveen is Tara's mother's cousin, which is option (b).
**Fast method (30 seconds):** Write the chain as arrows: Naveen, mother, brother, daughter, daughter (Tara). Cancel the first four steps into "cousin of Naveen". Tara is one generation below that cousin, so Tara sits one generation below Naveen's own level.
**Check:** Hand-checked (family tree with 3 generations).
**Explain simply:**
- Your mother's brother is your maternal uncle; his children are your cousins.
- Your cousin's child is not your cousin; she is one generation younger.
- The gender of Naveen is not given, so avoid "nephew" or "niece" words unless asked; "mother's cousin" works for any gender.
**Likely follow-ups:** 1) *What is Tara to Naveen?* The child of Naveen's cousin, i.e. Naveen's first cousin once removed (the reverse direction of the question). 2) *If the sentence said "Naveen's mother's only sister has a daughter, and she is Tara's mother"?* Same logic: that daughter is Naveen's cousin, so Naveen is again Tara's mother's cousin (hand-checked).
**Common mistakes / traps:** Choosing (c) "cousin" because the middle link was a cousin; choosing (d) "nephew" (that would make Tara an aunt or uncle of Naveen, but Tara is a generation younger) or (a) "maternal uncle" (that would need Naveen to be the brother of Tara's mother, not her cousin).
**If you are short of time (our suggestion):** Do not skip; draw the three-level tree. If a chain is longer than five links, guess only after you have cancelled two links.

### Q5 ⭐⭐⭐ 🟢 Mock Set 1, Q5 (suggested time 75 seconds): In a certain code, SALARY is written as UZNZTX. Using the same rule, how is LEAVES written?
**Asked at:** commonly asked (no company-specific report found); coding-decoding is listed among Mu Sigma logical-reasoning topics in prep-site summaries (reported, unverified).
**Target time:** 75 seconds (as in the heading).
**What the interviewer is checking:** Whether you compare letters position by position and find a repeating shift pattern, then apply it without slips.
**Say this in the interview:** "Compare SALARY and UZNZTX letter by letter: the shifts alternate plus 2, minus 1. Applying that to LEAVES gives NDCUGR."
**Answer:** **NDCUGR**
**Step-by-step reasoning:**
1. Compare letter by letter: S to U is +2; A to Z is -1; L to N is +2; A to Z is -1; R to T is +2; Y to X is -1. The pattern +2, -1, +2, -1, +2, -1 fits every one of the six letters.
2. Apply to LEAVES: L +2 = N; E -1 = D; A +2 = C; V -1 = U; E +2 = G; S -1 = R.
3. Result: N D C U G R.
**Fast method (30 seconds):** Write the alphabet position under each letter (S=19 to U=21), find the difference once for the first two letters, test it on the third and fourth. When the shift is odd-even alternating, the pattern is almost always repeating pairs.
**Check:** Verified by script: applying (+2, -1) to SALARY reproduces UZNZTX, and to LEAVES gives NDCUGR.
**Explain simply:**
- A "code" question hides one rule; find it from the example, then apply it.
- "+2" means move two letters forward in the alphabet (S, T, U).
- Check the rule on all letters of the example, not just the first two.
**Likely follow-ups:** 1) *What if a rule had the same shift for all letters?* Then the code is a plain shift (Caesar cipher), found from one letter. 2) *Decode "UZNZTX" without the example?* Apply the reverse shifts (-2, +1) to get SALARY.
**Common mistakes / traps:** Assuming a constant +1 or +2 shift after the first letter; forgetting that the pattern repeats and applying -1 twice in a row.
**If you are short of time (our suggestion):** Spend 20 seconds finding the rule; if nothing fits two letters, skip. If the shifts are known, always finish.

### Q6 ⭐⭐⭐ 🟢 Mock Set 1, Q6 (suggested time 75 seconds): A courier leaves a depot, rides 7 km east, 9 km north, 3 km west and then 6 km south. How far is the courier from the depot, and in the north-east, north-west, south-east or south-west direction from the depot?
**Asked at:** commonly asked (no company-specific report found); direction-sense items are a standard aptitude topic (prep-site claim, unverified).
**Target time:** 75 seconds (as in the heading).
**What the interviewer is checking:** Whether you add opposite moves into net east-west and north-south displacements and then use the right-angled triangle.
**Say this in the interview:** "East 7 minus west 3 is 4 east. North 9 minus south 6 is 3 north. So 4 east and 3 north, which is 5 km by the 3-4-5 triangle, in the north-east."
**Answer:** **5 km, north-east.**
**Step-by-step reasoning:**
1. East-west: +7 (east) and -3 (west) gives net 4 km east.
2. North-south: +9 (north) and -6 (south) gives net 3 km north.
3. Straight-line distance = square root of (4 squared + 3 squared) = square root of 25 = 5 km.
4. East and north components both positive, so the courier is north-east of the depot.
**Fast method (30 seconds):** Cancel opposite moves first; the 3-4-5 triple (and 5-12-13, 8-15-17) gives the distance without a calculator.
**Check:** Verified by script: net (4, 3), distance 5.0.
**Explain simply:**
- Distance means the straight line from start to end, not the 25 km ridden.
- Opposite directions subtract; perpendicular directions form the two sides of a right triangle.
- Pythagoras: the long side squared equals the sum of the two short sides squared.
**Likely follow-ups:** 1) *How far did the courier ride in total?* 7 + 9 + 3 + 6 = 25 km. 2) *If the last leg were 12 km south instead of 6?* Net 4 east, 3 south, still 5 km, now south-east (hand-checked: 9 - 12 = -3).
**Common mistakes / traps:** Giving 25 km or 7 + 9 = 16 as the distance; subtracting the wrong pair and ending up north-west.
**If you are short of time (our suggestion):** Do not skip; sketch a quick plus-sign and net out each axis. It should take under a minute.

### Q7 ⭐⭐ 🟡 Mock Set 1, Q7 (suggested time 60 seconds): A seating puzzle has 8 people and 7 clues. After two minutes of trying to place everyone, no arrangement is fixed. What decision rule would you apply in a timed online assessment, and what would you do first on the next attempt?
**Asked at:** commonly asked (no company-specific report found); skip-and-return advice is common on prep sites (prep-site claim, unverified). The rule below is our suggestion, not a research finding.
**Target time:** 60 seconds (as in the heading).
**What the interviewer is checking:** Whether you manage time like an analyst: stop sunk-cost effort, protect the easy marks, and return with a better method.
**Say this in the interview:** "After about two minutes with no fixed seat, I mark it for review and move on, because one puzzle should not cost me three easy questions. When I return, I start with the clues that fix a position, not with the loose ones."
**Answer:** **Rule (our suggestion): cap each puzzle at about two minutes with nothing fixed, flag it, move on, return only if time is left. On the next attempt, place the most definite clue first (fixed seat or end position), then build the skeleton from clues that link people.**
**Explain simply:**
- Sunk cost: time already spent does not make the next minute more likely to work.
- Rule of thumb only: with the sets here averaging about a minute and a quarter per question, one puzzle at 4 minutes costs roughly three other questions.
- Better start order for 8 people and 7 clues: (1) clues that name a fixed position (end seat, "third from left"); (2) clues with "exactly" or "immediately" (strong links); (3) negative clues ("not next to") last, to eliminate.
- Write a small table with 8 empty slots and put every certain fact in at once; do not hold clues in your head.
**Worked mini-example:** 8 seats, clues: A at an end, B immediately left of C, D not next to A. Place A at left end first (two cases). Then fit the pair B-C as a block. Last, remove cases where D is next to A. Testing the end-seat cases halves the search.
**Check:** This is a judgement rule, not a computed result; the 2-minute cap and the order of clues are our suggestion. The arithmetic (one 4-minute puzzle costs about three questions at about 75 seconds each) is hand-checked.
**Likely follow-ups:** 1) *How do you decide which skipped puzzle to return to?* Pick the one where you already fixed 2 or more seats. 2) *What if there is no negative marking?* Then guess the last 10 seconds instead of leaving it blank (our suggestion).
**Common mistakes / traps:** "Just five more minutes" thinking; reading all 7 clues again without writing; starting from the weakest ("not next to") clue.
**If you are short of time (our suggestion):** Skip it after the 2-minute cap, flag it, and guess only if a wrong answer costs nothing or the cost is small compared with the chance of being right.

### Q8 ⭐⭐ 🟡 Mock Set 1, Q8 (suggested time 90 seconds): If 1 March 2027 is a Monday, what day of the week is 27 June 2027?
**Asked at:** commonly asked (no company-specific report found); calendar items are a standard aptitude topic (prep-site claim, unverified).
**Target time:** 90 seconds (as in the heading).
**What the interviewer is checking:** Whether you count days and use remainder-after-7 arithmetic correctly, including month lengths.
**Say this in the interview:** "From 1 March to 27 June is 118 days. 118 divided by 7 leaves 6, so the weekday moves 6 forward from Monday, which is Sunday."
**Answer:** **Sunday**
**Step-by-step reasoning:**
1. Days from 1 March to 1 June: March 31 + April 30 + May 31 = 92 days.
2. From 1 June to 27 June: 26 more days. Total gap = 92 + 26 = 118 days.
3. 118 = 16 x 7 + 6, so the remainder is 6.
4. Monday plus 6 days = Sunday (Tue, Wed, Thu, Fri, Sat, Sun).
**Fast method (30 seconds):** Only the remainder after dividing by 7 matters. Reduce each month length first: 31 gives 3, 30 gives 2. So March 3 + April 2 + May 3 = 8, which is 1; plus 26 days = 26 mod 7 = 5; 1 + 5 = 6. Same answer, smaller numbers.
**Check:** Verified by script (Python date library): 1 March 2027 is a Monday, 27 June 2027 is a Sunday, gap 118 days.
**Explain simply:**
- Weekdays repeat every 7 days, so full weeks change nothing; only the leftover days count.
- Forward 6 days is the same as back 1 day (from Monday back to Sunday).
- 2027 is not a leap year, but the gap here starts after February, so it would not matter anyway.
**Likely follow-ups:** 1) *What weekday is 100 days after 1 March 2027?* 100 mod 7 = 2, so Wednesday (9 June 2027, script-checked). 2) *What day is 1 July 2027?* 4 days after Sunday 27 June, so Thursday (hand-checked).
**Common mistakes / traps:** Counting 27 June as 118 + 1; forgetting that the remainder is 6, not 7; using 30 days for every month.
**If you are short of time (our suggestion):** Do not skip if you remember the remainder-after-7 trick; if you cannot start in 20 seconds and options are given, avoid Monday (118 is not a multiple of 7).

### Q9 ⭐⭐ 🟡 Mock Set 1, Q9 (suggested time 90 seconds): Of 90 candidates in a hiring drive, 52 passed the SQL test, 47 passed the Excel test and 18 passed neither. How many passed both?
**Asked at:** commonly asked (no company-specific report found); two-set overlap counting is a standard aptitude item (prep-site claim, unverified).
**Target time:** 90 seconds (as in the heading).
**What the interviewer is checking:** Whether you use the union formula and notice that "neither" must be taken away from the total first.
**Say this in the interview:** "Passed at least one test is 90 minus 18, which is 72. SQL plus Excel is 99, so the overlap is 99 minus 72, which is 27."
**Answer:** **27 candidates passed both.**
**Step-by-step reasoning:**
1. Passed at least one test = 90 - 18 = 72.
2. Add the two pass counts: 52 + 47 = 99. Anyone who passed both is counted twice.
3. Both = 99 - 72 = 27.
4. Parts: SQL only 52 - 27 = 25; Excel only 47 - 27 = 20; both 27; neither 18. Total 25 + 20 + 27 + 18 = 90.
**Fast method (30 seconds):** Both = (A + B) - (Total - Neither). The double counting equals exactly the extra of 99 over 72.
**Check:** Verified by script: 52 + 47 - 72 = 27; region totals add to 90.
**Explain simply:**
- Union means "at least one"; the formula is |A or B| = A + B - both.
- "Neither" is outside both circles, so remove it before using the union.
- Always check by adding the four regions back to the total.
**Likely follow-ups:** 1) *How many passed only SQL?* 25. 2) *Variant: 80 candidates, 50 and 40 passed, 10 neither; both?* 50 + 40 - 70 = 20 (script-checked).
**Common mistakes / traps:** Doing 52 + 47 - 90 = 9 (forgetting the 18 who passed neither); answering 99 - 90 and treating the 18 as if they passed one test.
**If you are short of time (our suggestion):** Do not skip; it is a two-line formula. Guess only if the numbers are messy and you cannot start in 20 seconds.

### Q10 ⭐⭐ 🟡 Mock Set 1, Q10 (suggested time 75 seconds): A section gives +1 for a correct answer and -0.25 for a wrong one, and each question has 5 options. You can eliminate 2 options on a question and guess among the remaining 3. What is the expected mark from guessing, and should you guess?
**Asked at:** commonly asked (no company-specific report found); negative-marking decisions are a standard test-strategy topic (prep-site claim, unverified).
**Target time:** 75 seconds (as in the heading).
**What the interviewer is checking:** Whether you can compute an expected value and use it as a decision rule instead of a gut feeling.
**Say this in the interview:** "With 3 options left, I win 1 mark one time in three and lose 0.25 two times in three: 1/3 minus 1/6 is plus 0.167. That is positive, so I guess."
**Answer:** **Expected mark = +1/6, about +0.17 per guess. Yes, guess.**
**Step-by-step reasoning:**
1. Chance of being right among 3 options = 1/3; wrong = 2/3.
2. Expected mark = (1/3) x (+1) + (2/3) x (-0.25) = 0.3333 - 0.1667 = 0.1667.
3. Positive means that, over many such guesses, you gain marks on average.
**Fast method (30 seconds):** Break-even chance is 0.25 / (1 + 0.25) = 0.20, i.e. 1 in 5. Any guess better than 1-in-5 pays. With 5 options and no elimination the chance is exactly 1/5, so the expected mark is 0 (script-checked). Every eliminated option makes it positive.
**Check:** Verified by script with exact fractions: 1/3 - 1/6 = 1/6. Other cases: eliminating 1 option gives +0.0625; eliminating 3 gives +0.375.
**Explain simply:**
- Expected value means the average result if you repeated the same bet many times.
- A blind guess on a 5-option question with a -0.25 penalty is a fair bet (average zero); elimination tips it in your favour.
- Caution: an expected gain of 0.17 is an average. On one question you either gain 1 or lose 0.25. Your own elimination must be reliable for the 1/3 chance to be true.
**Likely follow-ups:** 1) *You can eliminate 1 option; guess?* Chance 1/4, expected +0.0625, a small gain (script-checked). 2) *No elimination; guess?* Expected 0, so it is a coin-flip on risk; our suggestion is to skip unless you want variance.
**Common mistakes / traps:** Using 1/5 after you have already eliminated options; subtracting 0.25 once instead of weighting it by the 2/3 chance of being wrong.
**If you are short of time:** Guess whenever you have removed at least 2 options; skip when you cannot remove any (our suggestion).

### Q11 ⭐⭐⭐ 🟡 Mock Set 2, Q1 (suggested time 75 seconds): Rules: "If a shift runs past midnight, the night allowance is doubled. If the night allowance is doubled, the supervisor signs the sheet." The supervisor has not signed Kabir's sheet. Which of these must be true? I. Kabir's allowance was not doubled. II. Kabir's shift did not run past midnight. III. Kabir's shift ran past midnight but the allowance was missed. Choose the correct set.
**Asked at:** commonly asked (no company-specific report found); if-then rules and the contrapositive are a standard logic topic (prep-site claim, unverified).
**Target time:** 75 seconds (as in the heading).
**What the interviewer is checking:** Whether you reason backwards through a chain of conditions using the contrapositive, not the converse.
**Say this in the interview:** "The chain is: past midnight leads to doubled allowance leads to signature. No signature means no doubled allowance, which means no past-midnight shift. So I and II are true, III is false."
**Answer:** **I and II must be true. III must be false.**
**Step-by-step reasoning:**
1. Rule A: past midnight implies doubled. Rule B: doubled implies supervisor signs.
2. Not signed. Contrapositive of B: not signed implies not doubled. So I is true.
3. Contrapositive of A: not doubled implies not past midnight. So II is true.
4. III says the shift did run past midnight; that contradicts II. So III is false.
**Fast method (30 seconds):** When the end of the chain is missing, go backwards: each "if P then Q" becomes "no Q means no P". Stay going back until the chain runs out.
**Check:** Verified by brute force over the 8 combinations of (past midnight, doubled, signed): only (no, no, no) obeys both rules with "not signed".
**Explain simply:**
- Contrapositive of "if P then Q" is "if not Q then not P"; it always has the same truth as the original.
- Converse ("if Q then P") and inverse ("if not P then not Q") are not equivalent to the original.
- Here: not signed rules out doubled, which in turn rules out past midnight.
**Likely follow-ups:** 1) *If the sheet had been signed, what follows?* Nothing about midnight or doubling: a signature can happen for other reasons (converse trap; a check of the 8 combinations shows 3 remain allowed). 2) *If Kabir's shift ran past midnight, what follows?* Doubled and signed, by the chain (hand-checked).
**Common mistakes / traps:** Choosing III "allowance was missed" (it needs a shift past midnight, which is ruled out); assuming "signed" is the only way a sheet can be signed (the converse fallacy).
**If you are short of time (our suggestion):** Do not skip; this is a one-line logic item. If the wording looks tangled, apply the contrapositive and still answer.

### Q12 ⭐⭐⭐ 🟡 Mock Set 2, Q2 (suggested time 120 seconds): Six interviewers P, Q, R, S, T and U sit in a row facing north, positions 1 to 6 from the left. R sits at one of the two ends. P does not sit at an end. Q sits somewhere to the right of R. S sits in position 3. T sits immediately between P and U (that is, P, T and U occupy three consecutive seats with T in the middle). Q and U are not neighbours. Who sits at the right end (position 6)?
**Asked at:** commonly asked (no company-specific report found); linear seating is a standard puzzle in aptitude gates (prep-site claim, unverified).
**Target time:** 120 seconds (as in the heading).
**What the interviewer is checking:** Whether you fix the strongest clue first and use block clues to place several people at once.
**Say this in the interview:** "S is fixed at 3. R is at an end, and Q is to R's right, so R must be on the left end, seat 1. The block P, T, U needs three consecutive seats with P not at an end. Only seats 4, 5, 6 remain, so P must be at 4 or 6; not at the end gives P at 4, T at 5, U at 6. That leaves Q at 2."
**Answer:** **U sits at the right end (position 6).**
**Step-by-step reasoning:**
1. S = seat 3 (given).
2. R is at an end. Q is to the right of R, so R cannot be at seat 6; R = seat 1.
3. Remaining people P, T, U, Q fill seats 2, 4, 5, 6. The block P-T-U with T in the middle needs three consecutive seats: only 4, 5, 6 (seat 3 is taken).
4. P is not at an end, so P = 4, T = 5, U = 6 (U at 4 and P at 6 would put P on the end).
5. Q gets seat 2. Check Q and U are not neighbours: seats 2 and 6, fine.
Final row (left to right):
| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| R | Q | S | P | T | U |
Unique because every step was forced; the brute-force search over all 720 orders found exactly one arrangement.
**Fast method (30 seconds):** Start with the fixed seat (S at 3), then the end clue (R, with "Q to the right" ruling out the right end), then place the 3-seat block into the only free stretch of seats.
**Check:** Verified by brute force over all 720 permutations: exactly one row passes all clues; re-read all seven clues against the table (R at end yes; P not at end yes; Q right of R yes; S at 3 yes; T between P and U yes; Q and U apart yes).
**Explain simply:**
- Facing north, left to right is the same as position 1 to 6 as given.
- A "block" clue ("T immediately between P and U") moves three people at once.
- "Right of" here means any seat further along, not necessarily the next one.
**Likely follow-ups:** 1) *If R could be at either end and Q needed no right-of-R rule?* More than one row would fit, so the answer would not be unique (do not guess). 2) *Who sits at position 2?* Q.
**Common mistakes / traps:** Putting R on the right end (then no seat is to its right for Q); allowing P-T-U to sit across seat 3 where S is.
**If you are short of time:** Our suggestion: this is a doable puzzle because two clues fix seats at once, so attempt it after the quick items; skip only if the first 2 clues do not fix a seat. If you must guess, remember that the right end cannot be R, S or P (R is at the left end, S at 3, P not at an end), leaving Q, T or U; T cannot be at an end either, so Q or U.

### Q13 ⭐⭐⭐ 🟡 Mock Set 2, Q3 (suggested time 120 seconds): Six colleagues A, B, C, D, E and F sit around a circular table facing the centre (a person facing the centre has their left hand towards the clockwise direction). A sits opposite D. B sits immediately to the left of D. E sits next to A. C does not sit next to B. F does not sit next to D. F sits immediately to the right of A. Who sits opposite E?
**Asked at:** commonly asked (no company-specific report found); circular seating is a standard puzzle in aptitude gates (prep-site claim, unverified).
**Target time:** 120 seconds (as in the heading).
**What the interviewer is checking:** Whether you handle left and right correctly when everyone faces the centre, and use "opposite" as seat plus 3.
**Say this in the interview:** "With six seats, opposite means three seats away. Facing the centre, a person's left is clockwise. Fix A, put D opposite, then F is on A's right (anti-clockwise from A), B on D's left (clockwise from D), E next to A on the other side, C takes what is left. E's opposite is B."
**Answer:** **B sits opposite E.**
**Step-by-step reasoning:**
1. Number the seats 0 to 5 clockwise and put A at 0. D is opposite A, so D = 3.
2. F is immediately to the right of A. Facing the centre, left is clockwise, so right is anticlockwise: F = 5.
3. B is immediately to the left of D, which is clockwise from D: B = 4.
4. E sits next to A. Seat 5 is F, so E = 1. C takes seat 2.
5. Check the neighbour clues: C (2) is next to E and D, not B (4), fine. F (5) is next to B (4) and A (0), not D (3), fine.
Clockwise order: A(0), E(1), C(2), D(3), B(4), F(5). Opposites: A-D, E-B, C-F.
**Fast method (30 seconds):** Fix one person at a seat, use "opposite = +3". Work out left/right by one rule written at the top of the page: facing in, left = clockwise. Placing the two pairs (A, D) and (A, F) gives four seats at once.
**Check:** Verified by brute force over all 120 arrangements with A fixed (so rotations are not counted twice): exactly one passes; re-read all seven clues against the final order.
**Explain simply:**
- At a round table facing the centre, your left hand points clockwise (as seen from above). This convention is stated in the question.
- Opposite seats are half-way round the table: three seats away for six people.
- Fixing one person removes the rotation duplicates; only relative positions matter.
**Likely follow-ups:** 1) *If F sat immediately to the LEFT of A instead (other clues unchanged)?* The unique table becomes A, F, C, D, B, E clockwise and the person opposite E is C (script-checked). 2) *Who sits between A and D going clockwise?* E and C.
**Common mistakes / traps:** Reversing left and right (that gives a different, inconsistent table); counting "opposite" as 2 seats away in a six-person ring.
**If you are short of time:** Our suggestion: do the quick items first and leave this for the last third of the set; it solves cleanly by fixing A, D and F once you have 2 minutes. If you must guess, A and D are opposite each other, so E's opposite is one of B, C or F.

### Q14 ⭐⭐⭐ 🟡 Mock Set 2, Q4 (suggested time 75 seconds): Three analysts A, B and C each say one thing. A: "Exactly one of us is lying." B: "Exactly two of us are lying." C: "All three of us are lying." Each person either always tells the truth or always lies. Who is telling the truth?
**Asked at:** commonly asked (no company-specific report found); truth-teller and liar items are a standard puzzle topic (prep-site claim, unverified).
**Target time:** 75 seconds (as in the heading).
**What the interviewer is checking:** Whether you test the possible number of liars and check each statement for self-consistency.
**Say this in the interview:** "The three statements name 1, 2 and 3 liars, so at most one can be true. C cannot be true, since C would then be one of three liars. If A were true, B and C would both be liars, which is two liars, not one. So B is the truthful one, and A and C lie."
**Answer:** **Only B is telling the truth.**
**Step-by-step reasoning:**
1. The three claims (exactly 1, exactly 2, all 3 liars) cannot be true together, so at most one person tells the truth.
2. If C told the truth, C would be one of 3 liars: contradiction. So C lies.
3. If nobody told the truth, there are 3 liars, which would make C right: contradiction.
4. So exactly one person is truthful: A or B. If A were truthful, there would be exactly 1 liar, but B and C both lie: contradiction. So B is truthful.
5. Check B: B says exactly two lie. A and C lie, and B tells the truth: two liars. True.
**Fast method (30 seconds):** Count the liars first, not the people. Each statement names a different number of liars, so at most one is true; try the possible counts (1, 2, 3, 0) and keep the count that makes the speaker of exactly that statement truthful.
**Check:** Verified by brute force over all 8 truth patterns: the only consistent pattern is (A lies, B truthful, C lies).
**Explain simply:**
- A truth-teller's statement must be true; a liar's statement must be false (not "partly" false).
- Use contradictions to rule options out: if a statement being true breaks itself, it must be false.
- The number of liars is a single fixed number, so statements naming different numbers cannot both be true.
**Likely follow-ups:** 1) *If A and B both said "exactly one of us is lying", C said "all three lie"?* Then A and B tell the truth and C lies (script-checked: unique). 2) *If all three said "exactly two of us are lying"?* Then 2 liars among 3 equal speakers is impossible (hand-checked: the same statement would be both true and false).
**Common mistakes / traps:** Assuming the first speaker is truthful and stopping; treating C's claim as possibly true; forgetting that a liar's statement must be false.
**If you are short of time (our suggestion):** Do not skip; try counts 1, 2, 3 in turn. This takes under a minute.

### Q15 ⭐⭐ 🟡 Mock Set 2, Q5 (suggested time 90 seconds): A decision table gives the discount on an order: order value of 10,000 or more and Gold member: 15%; 10,000 or more and not Gold: 10%; under 10,000 and Gold: 5%; under 10,000 and not Gold: 0%. Four orders are placed: (12,000, Gold), (9,500, Gold), (15,000, Silver) and (800, Silver). What is the total discount in rupees across the four orders?
**Asked at:** commonly asked (no company-specific report found); rule-table lookups appear in analyst screening tests (unverified).
**Target time:** 90 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you apply each row of a rule table to the right case without mixing up the two conditions.
**Say this in the interview:** "I will classify each order by value band and membership, apply the matching percentage, then add. The total is 3,775 rupees."
**Answer:** **Rs 3,775.**
**Step-by-step reasoning:**
1. (12,000, Gold): 12,000 is at least 10,000 and Gold, so 15%: 1,800.
2. (9,500, Gold): under 10,000 and Gold, so 5%: 475.
3. (15,000, Silver): at least 10,000, not Gold (Silver counts as not Gold), so 10%: 1,500.
4. (800, Silver): under 10,000, not Gold, so 0%: 0.
5. Total = 1,800 + 475 + 1,500 + 0 = 3,775.
**Fast method (30 seconds):** Write the pair "band, member" next to each order and read the percentage straight off the table; do not recompute the table. Watch the boundary: "10,000 or more" includes exactly 10,000 (no order sits on it here).
**Check:** Verified by script (1,800 + 475 + 1,500 + 0 = 3,775).
**Explain simply:**
- A "decision table" lists every combination of conditions and one result for each; exactly one row applies to each order.
- Any non-Gold tier (Silver here) falls in the "not Gold" rows.
**Likely follow-ups:** 1) *What if the 9,500 order were 10,000?* It moves to the 15% row: 1,500 instead of 475, total 4,800. 2) *Which order gets the highest percentage?* The 12,000 Gold order (15%).
**Common mistakes / traps:** Treating 9,500 as "near enough" to 10,000, or giving Silver a Gold rate; the tempting wrong totals come from using 15% for both large orders.
**If you are short of time (our suggestion):** Do not skip; it is a pure lookup. Four quick lookups take under a minute, so bank it early.

### Q16 ⭐⭐ 🟡 Mock Set 2, Q6 (suggested time 90 seconds): Trace the pseudocode and give the final value of total.
total = 0
for i = 1 to 6:
    if i is even: total = total + i
    else if i is divisible by 3: total = total - 1
    else: total = total + 1
**Asked at:** commonly asked (no company-specific report found); loop tracing is a standard pseudocode-logic item (unverified).
**Target time:** 90 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Careful, ordered tracing of a branching loop, especially the order of the tests (even is checked first).
**Say this in the interview:** "I will trace it in a small table, one row per i, checking even first, then divisible by 3. The final total is 13."
**Answer:** **total = 13.**
**Step-by-step reasoning:**
| i | branch taken | total after |
|---|---|---|
| 1 | odd, not divisible by 3: +1 | 1 |
| 2 | even: +2 | 3 |
| 3 | odd, divisible by 3: -1 | 2 |
| 4 | even: +4 | 6 |
| 5 | odd, not divisible by 3: +1 | 7 |
| 6 | even (checked first, so the "divisible by 3" branch is skipped): +6 | 13 |
**Fast method (30 seconds):** Evens add 2 + 4 + 6 = 12; the odd values 1, 3, 5 add +1, -1, +1 = +1; so 12 + 1 = 13.
**Check:** Verified by script (running the loop gives 13).
**Explain simply:**
- "else if" means the second test runs only when the first one failed, so 6 never reaches the "divisible by 3" test.
- Tracing means writing the variable after every pass instead of holding it in your head.
**Likely follow-ups:** 1) *What if the first test were "divisible by 3" instead of "even"?* Then i = 3 gives -1 and i = 6 gives -1, so the total would be 1 + 2 - 1 + 4 + 1 - 1 = 6 (hand-checked). 2) *What if the loop ran to 7?* i = 7 is odd and not divisible by 3, so 14.
**Common mistakes / traps:** Subtracting 1 at i = 6 because 6 is divisible by 3 (that gives 6 instead of 13), or stopping the loop at 5.
**If you are short of time (our suggestion):** Do it early; it is a safe, mechanical mark. Never guess it, trace it.

### Q17 ⭐⭐ 🟡 Mock Set 2, Q7 (suggested time 75 seconds): A table scores has one column score with the values 10, 20, NULL, 30, NULL (five rows). How many rows does SELECT * FROM scores WHERE score <> 20 OR score IS NULL return?
**Asked at:** commonly asked (no company-specific report found); NULL behaviour in WHERE is a classic SQL screening trap (unverified).
**Target time:** 75 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you know that comparing NULL to anything gives "unknown", and that WHERE keeps only rows that are TRUE.
**Say this in the interview:** "NULL <> 20 is unknown, not true, so the first condition drops the NULL rows, but IS NULL brings them back. So 10, 30 and both NULLs: 4 rows."
**Answer:** **4 rows** (10, NULL, 30, NULL).
**Step-by-step reasoning:**
1. Row 10: 10 <> 20 is TRUE, kept.
2. Row 20: 20 <> 20 is FALSE and it is not NULL, dropped.
3. Rows NULL: NULL <> 20 is UNKNOWN (not true), but score IS NULL is TRUE; UNKNOWN OR TRUE is TRUE, kept (both rows).
4. Row 30: TRUE, kept.
Real output from sqlite3 (run here):
```
SELECT * FROM scores WHERE score <> 20 OR score IS NULL;
-> 10, NULL, 30, NULL   (4 rows)
SELECT * FROM scores WHERE score <> 20;
-> 10, 30               (2 rows)
```
**Fast method (30 seconds):** "Everything except the 20" = 5 - 1 = 4, because the OR IS NULL clause rescues the NULLs.
**Check:** Verified by running both queries in Python's sqlite3. Other databases follow the same standard three-valued logic (from memory, not run here; confirm in the tool).
**Explain simply:**
- NULL means "no value known"; asking whether an unknown equals or differs from 20 has no yes/no answer, so SQL says UNKNOWN.
- WHERE keeps a row only when its condition is TRUE, so UNKNOWN rows vanish unless another condition rescues them.
**Likely follow-ups:** 1) *What does WHERE score <> 20 alone return?* 2 rows (10 and 30). 2) *What does WHERE score = NULL return?* 0 rows; use IS NULL.
**Common mistakes / traps:** Answering 2 (forgetting the NULLs) or 3 (counting only one NULL).
**If you are short of time (our suggestion):** Do it; it is a one-line logic item. If blank, answer 4, the standard "all except 20" result.

### Q18 ⭐⭐ 🟡 Mock Set 2, Q8 (suggested time 75 seconds): After a new training module was introduced, the average ticket resolution time fell by 12%. Which one of these, if true, most weakens the claim that the module caused the fall?
Options: (a) Average resolution time also fell by about 12% over the same period in teams that never took the module. (b) The module cost 2 lakh rupees to build. (c) Agents rated the module highly in a survey. (d) A few agents completed the module more slowly than others.
**Asked at:** commonly asked (no company-specific report found); cause-and-effect weakening items are a standard critical-reasoning type (unverified).
**Target time:** 75 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you look for a comparison group (a control) before accepting "after, therefore because".
**Say this in the interview:** "If teams without the module improved by the same 12%, something else explains the fall. That is option (a)."
**Answer:** **(a).**
**Step-by-step reasoning:**
1. The claim is "the module caused the fall". To weaken a causal claim, show the effect appears without the cause.
2. (a) does exactly that: teams with no module saw the same 12% fall, so the module adds nothing visible; a common outside factor (seasonal drop in ticket volume, a new tool, easier tickets) is likelier.
3. (b) is about cost, not cause: irrelevant (scope shift).
4. (c) is about opinion, not resolution time; if anything it mildly supports the module.
5. (d) says some agents finished the course slowly; that does not touch whether the fall was caused by the module.
**Fast method (30 seconds):** For "caused" arguments, ask "what happened to the group that did NOT get the treatment?" The option that answers this is usually the one.
**Check:** Each option was tested against one question: does it make the 12% fall likely without the module? Only (a) does. Hand-checked.
**Explain simply:**
- A "control group" is a similar group that did not get the change; it shows what would have happened anyway.
- "After" does not prove "because of" (correlation is not causation).
**Likely follow-ups:** 1) *What would strengthen the claim?* Teams without the module showed no fall. 2) *What data would settle it?* Compare module-takers with similar non-takers, before and after (a difference-in-differences style comparison).
**Common mistakes / traps:** Picking (c) or (d) because they sound related to the module; cost (b) is a distractor about value, not cause.
**If you are short of time (our suggestion):** Do not skip; reasoning-style items are quick marks. If you must guess, pick the option that mentions a group without the module.

### Q19 ⭐⭐ 🟡 Mock Set 2, Q9 (suggested time 60 seconds): After 6 minutes on Mock Set 2, Q2 (a seating row) still is not solved, 4 questions remain unattempted and the set has 9 minutes left. Explain what you do, with the time you give each remaining question, and why.
**Asked at:** commonly asked (no company-specific report found); skip and time-split advice appears on prep sites (reported, unverified), and the splits below are our suggestion, not a research finding.
**Target time:** 60 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you can cut a loss: stop spending time on a sunk puzzle and spread the remaining time sensibly.
**Say this in the interview:** "I stop now, mark the row for review, and give the four remaining questions about two minutes each, keeping one minute in reserve to return to the row only if time is left."
**Answer:** **Abandon the row (mark for review), spend about 2 minutes on each of the 4 remaining questions (8 minutes), and use the last minute to revisit or to guess the row.** (Our suggestion.)
**Step-by-step reasoning:**
1. Six minutes on one item is far above its share (its suggested time is 2 minutes); the time already spent is gone whatever you do ("sunk cost").
2. 9 minutes divided over 4 fresh questions is 2.25 minutes each, so a 2-minute cap each leaves a 1-minute buffer.
3. Within the four, take the quickest first (one-line logic, tracing), so easy marks are banked before time runs out.
4. If the buffer remains, reread the row clues once with fresh eyes; otherwise guess an option (check whether the test has negative marking, and guess only after eliminating options).
**Fast method (30 seconds):** Remaining minutes divided by remaining questions gives your per-question cap; if one item already exceeded its cap, drop it.
**Check:** Arithmetic: 4 x 2 = 8 minutes, 9 - 8 = 1 minute reserve (hand-checked).
**Explain simply:**
- "Sunk cost" means time already spent that you cannot get back; it should not decide what you do next.
- Marking for review lets you return only if time remains.
**Likely follow-ups:** 1) *What if the 4 remaining were all hard?* Give the two you can start fastest 3 minutes each and guess or skip the rest. 2) *What if there were no mark-for-review button?* Pick your best guess for the row now and move on.
**Common mistakes / traps:** "Just one more minute" on the row, which steals time from four questions that are likelier to be solved.
**If you are short of time (our suggestion):** This is itself the skip rule: skip the stuck puzzle, guess it only at the end, and never let one item take more than about twice its suggested time.

### Q20 ⭐⭐ 🔴 Mock Set 2, Q10 (suggested time 120 seconds): In a round-robin tournament each of 5 teams plays every other team exactly once and there are no draws. All five teams finish with different numbers of wins. How many wins did the team in third place have, and how do you know the full list of win counts is forced?
**Asked at:** commonly asked (no company-specific report found).
**Target time:** 120 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Counting-total reasoning: total wins is fixed, and distinct values in a small range leave only one possibility.
**Say this in the interview:** "There are 10 matches, so 10 wins in total. Five different win counts, each between 0 and 4, must be 0, 1, 2, 3, 4, which sums to 10. Third place has 2."
**Answer:** **2 wins** (the full list is 4, 3, 2, 1, 0).
**Step-by-step reasoning:**
1. Number of matches = 5 x 4 / 2 = 10; with no draws each match gives exactly one win, so the wins add up to 10.
2. A team plays 4 matches, so its wins are a whole number from 0 to 4.
3. Five teams with five different values from {0, 1, 2, 3, 4} must use each value exactly once.
4. Check the sum: 0 + 1 + 2 + 3 + 4 = 10, which matches the total (so the list is consistent, and it is the only list possible).
5. Ordered from the top: 4, 3, 2, 1, 0, so third place has 2 wins.
**Fast method (30 seconds):** Five distinct values in a range of exactly five values means all of them are used; third of five in order is the middle value, 2.
**Check:** Verified by brute force over all 2^10 = 1,024 outcome sets: every outcome with five different win counts has the sorted list 4, 3, 2, 1, 0 (and such outcomes exist).
**Explain simply:**
- A "round robin" means every pair meets once; the handshake count n(n-1)/2 gives the matches.
- The "range trick": if you need k different whole numbers inside a range of exactly k values, you must use them all.
**Likely follow-ups:** 1) *Who beat whom?* The 4-win team beat all; the 3-win team beat everyone except the top team; and so on down (a perfectly ranked tournament). 2) *What changes with 6 teams?* Wins range 0 to 5 and total 15, and 0 + 1 + 2 + 3 + 4 + 5 = 15, so it is again forced (hand-checked arithmetic).
**Common mistakes / traps:** Forgetting that a team plays only 4 matches (so 5 wins is impossible), or hunting for a pattern in the results instead of using the total.
**If you are short of time (our suggestion):** Do it if you spot the range trick; it takes 30 seconds. If not, guess 2 (the middle of 0 to 4).

### Q21 ⭐⭐⭐ 🟡 Mock Set 3, Q1 (suggested time 75 seconds): Statements: Some auditors are coders. No coder is a trainee. All trainees are interns. Conclusions: I. Some auditors are not trainees. II. Some coders are not trainees. III. No intern is a coder. Which conclusions follow?
**Asked at:** commonly asked (no company-specific report found); syllogisms are reported on prep sites for service-company and analytics-firm tests (unverified).
**Target time:** 75 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you separate what the statements force from what merely looks likely.
**Say this in the interview:** "The auditors who are coders cannot be trainees, so I and II follow. III does not: some interns could still be coders, because only trainee interns are ruled out."
**Answer:** **Only I and II follow; III does not.** (Convention: every named group has at least one member; "some" means at least one.)
**Step-by-step reasoning:**
1. "Some auditors are coders" gives at least one person who is both auditor and coder.
2. "No coder is a trainee": that person is not a trainee. So some auditors are not trainees (I) and some coders are not trainees (II, in fact all coders).
3. "All trainees are interns" only puts trainees inside interns; it says nothing about the interns who are not trainees.
4. So a coder who is an intern but not a trainee is consistent: III ("No intern is a coder") is not forced.
**Fast method (30 seconds):** Draw circles: Coder and Trainee do not overlap; Trainee sits inside Intern; Coder may still overlap the rest of Intern. A conclusion follows only if it is true in every such picture.
**Check:** Verified by script: all possible region-occupancy models were enumerated; I and II hold in every model, III fails in some.
**Explain simply:**
- "Follows" means true in every situation that fits the statements, not just in one picture.
- A group inside another (trainees inside interns) does not make the outer group share the inner group's rules.
**Likely follow-ups:** 1) *What if the third statement were "All interns are trainees"?* Then no coder could be an intern, so III would follow (hand-checked). 2) *Does "Some coders are not auditors" follow?* No; the statements do not say.
**Common mistakes / traps:** Marking III because "coders and trainees are separate and trainees are interns", which slides from "no trainee" to "no intern".
**If you are short of time (our suggestion):** Do not skip; syllogisms are quick marks. Under negative marking, answer I and II only if you are confident; they are the safe, forced ones.

### Q22 ⭐⭐⭐ 🔴 Mock Set 3, Q2 (suggested time 150 seconds): Four analysts Asha, Bilal, Chen and Dina each use a different tool from Excel, SQL, Python and Tableau and each live in a different city from Pune, Delhi, Chennai and Kochi. Asha does not use SQL and does not live in Delhi. The Python user lives in Pune. Bilal lives neither in Kochi nor in Pune. The Tableau user does not live in Chennai. Chen does not use Excel. Either Asha lives in Kochi or Dina uses SQL (or both). The Excel user lives in Kochi. Dina does not live in Pune. Bilal does not use Tableau. Which tool does Dina use and in which city does she live?
**Asked at:** commonly asked (no company-specific report found); matching grids are a reported puzzle type on prep sites (unverified).
**Target time:** 150 seconds (rule of thumb, as written in the heading); per the Set 3 strategy, keep a two-minute rule.
**What the interviewer is checking:** Whether you can chain clues into a grid and spot the clue that pins down a person.
**Say this in the interview:** "Python is Pune and Excel is Kochi, so Tableau and SQL share Delhi and Chennai; Tableau is not Chennai, so Tableau is Delhi and SQL is Chennai. Then the people fall into place: Dina uses Tableau in Delhi."
**Answer:** **Dina uses Tableau and lives in Delhi.**
**Step-by-step reasoning:**
1. Python = Pune and Excel = Kochi (given). So SQL and Tableau are in Delhi and Chennai.
2. The Tableau user is not in Chennai, so Tableau = Delhi and SQL = Chennai.
3. Bilal is not in Kochi or Pune, so Bilal is in Delhi or Chennai, and he does not use Tableau, so Bilal = SQL, Chennai.
4. Dina is not in Pune, so Dina is not the Python user. Chen does not use Excel. Remaining people for Python, Excel, Tableau: Asha, Chen, Dina. Asha is not in Delhi, so Asha is not Tableau; Asha is Python or Excel.
5. Dina is not Python (step 4), and Dina does not use SQL (Bilal does), so the clue "Asha lives in Kochi or Dina uses SQL" forces Asha = Kochi = Excel.
6. Chen is then Python (Pune) or Tableau, and Dina is not Python, so Chen = Python, Pune and Dina = Tableau, Delhi.
| Analyst | Tool | City |
|---|---|---|
| Asha | Excel | Kochi |
| Bilal | SQL | Chennai |
| Chen | Python | Pune |
| Dina | Tableau | Delhi |
Unique because every step was forced; no choice was ever left open.
**Fast method (30 seconds):** Start with the two clues that tie a tool to a city (Python = Pune, Excel = Kochi); this leaves a 2 by 2 block that the Tableau clue breaks.
**Check:** Verified by brute force over all 24 x 24 = 576 tool/city assignments: exactly one satisfies every clue, the table above.
**Explain simply:**
- A matching grid pairs three lists; once two lists are tied together (tool and city), you only have to place the names.
- An "either or (or both)" clue is useful only after you have ruled out one side.
**Likely follow-ups:** 1) *If the clue "Dina does not live in Pune" were removed, is it still unique?* No: the enumeration then finds 2 solutions (the second has Chen on Tableau in Delhi and Dina on Python in Pune), so that clue is what makes it unique. 2) *Who lives in Kochi?* Asha.
**Common mistakes / traps:** Treating the "either or" clue as telling you Asha is in Kochi right away; it only bites after Dina is shown not to use SQL.
**If you are short of time (our suggestion):** Skip it if no start after 20 to 30 seconds; with four people you can also guess, but a wrong answer costs marks under negative marking. Do the quick items first.

### Q23 ⭐⭐⭐ 🔴 Mock Set 3, Q3 (suggested time 150 seconds): Five candidates A, B, C, D and E are interviewed one per day from Monday to Friday. A is interviewed on Monday. Exactly one candidate is interviewed between B and D, and B is interviewed before D. C is interviewed after D. A and C are not interviewed on consecutive days. E is not interviewed on Friday. Who is interviewed on Wednesday?
**Asked at:** commonly asked (no company-specific report found); scheduling puzzles are a reported type on prep sites (unverified).
**Target time:** 150 seconds (rule of thumb, as written in the heading); keep a two-minute rule.
**What the interviewer is checking:** Whether you place the fixed fact first and test the few remaining slots for the constrained pair.
**Say this in the interview:** "A is Monday, so B, D and C use Tuesday to Friday with B, one gap, D, then C after. That forces B Tuesday, D Thursday, C Friday, so E is Wednesday."
**Answer:** **E is interviewed on Wednesday.**
**Step-by-step reasoning:**
1. A = Monday, leaving Tuesday to Friday for B, C, D, E.
2. B is before D with exactly one candidate between them, so D is two days after B. C is after D.
3. Options for (B, D): (Tue, Thu) or (Wed, Fri). If D is Friday, C cannot be after D, so only (Tue, Thu).
4. C is after Thursday, so C = Friday. A (Monday) and C (Friday) are not consecutive, fine.
5. E takes the remaining day, Wednesday (and E is not on Friday, fine); the candidate between B and D is E.
| Mon | Tue | Wed | Thu | Fri |
|---|---|---|---|---|
| A | B | E | D | C |
Unique because only one (B, D) pair leaves room for C after D.
**Fast method (30 seconds):** "C after D" kills the pair with D on Friday; that leaves one pair and the rest is forced.
**Check:** Verified by brute force over all 120 orderings: exactly one satisfies all clues (A, B, E, D, C).
**Explain simply:**
- "Exactly one candidate between" means the two are two days apart.
- Using "after" clues to eliminate the last day for the earlier person is a standard schedule trick.
**Likely follow-ups:** 1) *If C were allowed Tuesday (no "after D" clue)?* Verified by script: 2 orderings would then fit, so the answer would no longer be unique. 2) *Who is interviewed on Thursday?* D.
**Common mistakes / traps:** Forgetting the "B before D" direction and trying D Tuesday; or answering C for Wednesday by ignoring "C after D".
**If you are short of time (our suggestion):** Attempt only after the quick items; with a 2-minute cap. If time is gone, guess E, since the middle slot is the one nobody else can take.

### Q24 ⭐⭐⭐ 🟡 Mock Set 3, Q4 (suggested time 120 seconds): A machine rearranges numbers in steps. Step 1 swaps the largest number with the number in position 1. Step 2 swaps the smallest number with the number in the last position. Step 3 swaps the largest of the numbers in positions 2 to 4 with the number in position 2, and so on. Input: 17 48 93 26 71. What is the arrangement after Step 2, and how many steps in total are needed to reach the final arrangement?
**Asked at:** commonly asked (no company-specific report found); input-output machine rearrangement is a reported banking-exam type (unverified).
**Target time:** 120 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you follow a procedure literally and notice the pattern (a sort in disguise) that tells you when it ends.
**Say this in the interview:** "Step 1 brings 93 to the front, step 2 sends 17 to the back, step 3 puts 71 in position 2. After step 2 it reads 93 48 71 26 17 and the final order is reached after 3 steps."
**Answer:** **After Step 2: 93 48 71 26 17. Total steps needed: 3** (final arrangement 93 71 48 26 17, descending order).
**Step-by-step reasoning:**
| Step | Rule | Result |
|---|---|---|
| Input | | 17 48 93 26 71 |
| 1 | largest (93) swaps with position 1 (17) | 93 48 17 26 71 |
| 2 | smallest (17) swaps with last position (71) | 93 48 71 26 17 |
| 3 | largest of positions 2 to 4 (48, 71, 26 gives 71) swaps with position 2 (48) | 93 71 48 26 17 |
1. After Step 3 the list is in descending order, with 48 26 already in order.
2. A Step 4 (smallest of positions 3 to 4, swapped with the last of that range) would change nothing, so it is not needed.
3. So the final arrangement is reached at Step 3: 3 steps.
**Fast method (30 seconds):** Sort the input descending in your head (93 71 48 26 17) as the target; then count how many steps are needed to place each number in turn (93, 17, 71; the remaining two are already right).
**Check:** Verified by script (simulated alternating steps; the list is sorted descending after Step 3 and Step 4 makes no change).
**Explain simply:**
- Each step fixes one number at one end, then shrinks the range, like a two-ended selection sort.
- "Final arrangement" means the point after which no step changes anything.
**Likely follow-ups:** 1) *What if the input were 5 4 3 2 1?* It is already descending, so 0 steps are needed (hand-checked; each swap would swap an item with itself). 2) *What does the machine do in general?* It sorts into descending order.
**Common mistakes / traps:** Swapping the smallest number with position 2 instead of the last position, or counting a Step 4 that changes nothing.
**If you are short of time (our suggestion):** Do the two-step part (the arrangement after Step 2) first; if you cannot finish the step count, answer 3, since a 5-number list is sorted in at most 4 steps and the descending target shows 3.

### Q25 ⭐⭐ 🟡 Mock Set 3, Q5 (suggested time 90 seconds): Starting at point O facing north, a surveyor walks 4 km, turns left and walks 9 km, then turns left again and walks 16 km. How far is the surveyor from O, and in which direction from O?
**Asked at:** commonly asked (no company-specific report found); direction-and-distance items are reported on prep sites (unverified).
**Target time:** 90 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Turning left and right correctly and using coordinates plus the Pythagoras rule.
**Say this in the interview:** "Facing north, left is west, then left again is south. Net position is 9 west and 12 south, a 9-12-15 right triangle, so 15 km south-west."
**Answer:** **15 km, towards the south-west.**
**Step-by-step reasoning:**
1. Facing north: walk 4 km north. Position (0, 4) (x is east, y is north).
2. Turn left from north, which is west; walk 9 km: (-9, 4).
3. Turn left from west, which is south; walk 16 km: (-9, -12).
4. Distance from O = square root of (9 squared + 12 squared) = square root of 225 = 15 km.
5. x is negative (west) and y is negative (south), so the direction is south-west.
**Fast method (30 seconds):** Net north-south is 4 - 16 = 12 km south; east-west is 9 km west; 9-12-15 is a multiple of the 3-4-5 triple, so 15 km.
**Check:** Verified by script (position (-9, -12), distance 15.0).
**Explain simply:**
- Turning "left" depends on which way you face: left of north is west, left of west is south.
- A 3-4-5 right triangle (and its multiples such as 9-12-15) gives whole-number distances.
**Likely follow-ups:** 1) *What if the second turn were right instead?* Facing west, a right turn points north, so you walk north 16 km: (-9, 4 + 16) = (-9, 20), distance square root of 481 (about 21.9 km), north-west (script-checked). 2) *Which way would he face at the end?* South.
**Common mistakes / traps:** Turning left from north to east (mirror error), or adding 4 + 16 instead of subtracting; saying south-east.
**If you are short of time (our suggestion):** Do not skip; sketch it with a compass cross in 20 seconds. If you must guess, remember that 9-12-15 means 15 km.

### Q26 ⭐⭐ 🟡 Mock Set 3, Q6 (suggested time 75 seconds): Trace the pseudocode and give the final values of x and y.
x = 5; y = 1
while x > 0:
    y = y * x
    x = x - 2
**Asked at:** commonly asked (no company-specific report found); while-loop tracing is a standard pseudocode item (unverified).
**Target time:** 75 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you check the loop condition before every pass and know when the loop stops (including the value of x after the last pass).
**Say this in the interview:** "The loop runs for x = 5, 3, 1; y becomes 5, 15, 15. Then x becomes -1, the test fails, and the loop ends. So x = -1 and y = 15."
**Answer:** **x = -1 and y = 15.**
**Step-by-step reasoning:**
| Check x > 0 | y after y * x | x after x - 2 |
|---|---|---|
| 5 > 0 yes | 1 x 5 = 5 | 3 |
| 3 > 0 yes | 5 x 3 = 15 | 1 |
| 1 > 0 yes | 15 x 1 = 15 | -1 |
| -1 > 0 no | loop ends | |
**Fast method (30 seconds):** y is the product of the odd numbers 5 x 3 x 1 = 15; x ends one step below zero at -1.
**Check:** Verified by script (final x = -1, y = 15).
**Explain simply:**
- A while loop tests its condition before each pass; the test that fails is the last thing that happens, and x has already been changed by the last pass.
- Always report the final value of the counter too if asked, not only the result variable.
**Likely follow-ups:** 1) *What if the start were x = 6?* The loop runs for 6, 4, 2 and y = 48, final x = 0 (hand-checked). 2) *What if x = x - 1?* y = 120 (5 factorial) and x = 0.
**Common mistakes / traps:** Giving x = 1 (the last value used) instead of -1, or stopping after x = 3.
**If you are short of time (our suggestion):** Do not skip; it is quick. Both values are needed; if you guess, remember x does not stop at 1.

### Q27 ⭐⭐ 🟡 Mock Set 3, Q7 (suggested time 75 seconds): In Excel, cell A1 contains 7, cell B1 is completely empty and cell C1 contains 12. What does =IF(AND(A1>5, OR(B1="", C1<10)), "Y", "N") return, and why?
**Asked at:** commonly asked (no company-specific report found); nested IF/AND/OR logic is a typical spreadsheet screening item (unverified).
**Target time:** 75 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you evaluate nested logic inside out and know how Excel treats an empty cell in a comparison with "".
**Say this in the interview:** "A1 > 5 is true. B1 is empty, and an empty cell equals the empty text, so OR is true even though C1 < 10 is false. AND of two trues gives Y."
**Answer:** **"Y".**
**Step-by-step reasoning:**
1. A1 > 5: 7 > 5 is TRUE.
2. B1 = "": an empty cell is treated as equal to empty text, so TRUE.
3. C1 < 10: 12 < 10 is FALSE.
4. OR(TRUE, FALSE) is TRUE (one true is enough).
5. AND(TRUE, TRUE) is TRUE, so IF returns "Y".
**Fast method (30 seconds):** Work from the inside out; the OR only needs one true input, and B1="" already is.
**Check:** Hand-checked (Excel is not available here). The empty-cell equals "" behaviour is from memory, not run here; confirm in the tool (ISBLANK(B1) also returns TRUE for a truly empty cell).
**Explain simply:**
- AND needs all parts true; OR needs at least one.
- A cell with nothing in it is "blank"; Excel lets blank equal "" in a comparison, but a cell with a formula returning "" is not blank (ISBLANK would say FALSE) even though B1="" is still TRUE.
**Likely follow-ups:** 1) *What if B1 contained a space?* B1="" is then FALSE, OR falls to C1 < 10 which is FALSE, so the result is "N" (from memory, confirm in the tool). 2) *What if C1 were 8?* Y either way.
**Common mistakes / traps:** Saying N because C1 < 10 is false, forgetting that OR is satisfied by the blank test.
**If you are short of time (our suggestion):** Do it if you remember the blank rule; if not, the AND/OR logic still points to Y as the more likely answer.

### Q28 ⭐⭐ 🔴 Mock Set 3, Q8 (suggested time 90 seconds): "Regions with more sales reps have higher sales, so adding reps to a region will raise its sales." Why does the data not support this conclusion, and what two alternative explanations would you test first?
**Asked at:** commonly asked (no company-specific report found); correlation versus cause is a standard analyst interview and critical-reasoning theme (unverified).
**Target time:** 90 seconds (rule of thumb, as written in the heading).
**What the interviewer is checking:** Whether you can separate "regions with more reps have higher sales" (an association across regions) from "adding reps will raise sales" (a cause).
**Say this in the interview:** "The data shows the two move together, not that one drives the other. Maybe big markets get more reps (reverse direction), or a third factor like market size drives both. I would test those first."
**Answer:** **The argument jumps from a correlation across regions to a cause within one region; test (1) reverse causality, (2) a hidden third factor such as market size.**
**Worked mini-example (made-up numbers, for illustration):** Region North has 40 reps and Rs 8 crore of sales; Region East has 10 reps and Rs 2 crore. Sales per rep is the same, Rs 20 lakh. North may simply be a bigger market that earned more reps; adding 10 reps to East may not move it to Rs 4 crore.
**Explain simply:**
- Correlation means two things move together; causation means one makes the other change. Data across regions tells you only the first.
- Reverse causality: high sales may have led the company to hire more reps there.
- Confounder: a third factor (market size, population, number of customers, product mix) that raises both reps and sales.
- A better test: compare the same region before and after adding reps, or run a pilot with some regions getting extra reps and similar ones not (a controlled comparison).
**Check:** The example numbers are invented: 8 crore / 40 reps = 20 lakh and 2 crore / 10 reps = 20 lakh (hand-checked).
**Likely follow-ups:** 1) *What data would you pull first?* Sales and reps per region over time, plus market size and customer counts. 2) *What metric would you use?* Sales per rep, and the change in sales after rep additions compared with similar regions that added none.
**Common mistakes / traps:** Accepting the claim because the correlation is strong, or listing two explanations that are the same idea (for example "other factors" twice); name reverse causality and a confounder separately.
**If you are short of time (our suggestion):** Do not skip; you can answer in two sentences (correlation is not cause; market size or reverse direction). If it is an option-type item, pick the answer that points out the missing comparison.

### Q29 ⭐⭐ 🔴 Mock Set 3, Q9 (suggested time 90 seconds): From 7 interviewers, a panel of exactly 3 is chosen. Two particular interviewers, X and Y, cannot both be on the panel. How many different panels are possible?
**Asked at:** commonly asked (no company-specific report found); counting with a restriction is a standard reasoning item (prep-site claim, unverified).
**What the interviewer is checking:** Whether you count "all minus forbidden" instead of listing panels.
**Say this in the interview:** "All panels is 7 choose 3, which is 35. Panels with both X and Y: pick the third from the other 5, so 5. 35 minus 5 is 30."
**Answer:** **30 panels**
**Target time:** 90 seconds (as written in the heading).
**If you are short of time (our suggestion):** do it if it is the "all minus bad" type (it is, about 30 seconds); it is a safe quick mark, never skip it.
**Step-by-step reasoning:**
1. Panels with no restriction: "7 choose 3" means the number of ways to pick 3 people from 7 when order does not matter = (7 x 6 x 5) / (3 x 2 x 1) = 35.
2. Forbidden panels contain both X and Y. The third seat can be any of the other 5 people, so 5 forbidden panels.
3. Allowed = 35 - 5 = 30.
**Fast method (30 seconds):** "Total minus forbidden" is quicker than building the allowed cases, because the forbidden case is tiny.
**Check:** Verified by script: 35 total, 5 forbidden, 30 allowed; the other route (3 from the 5 others = 10, plus X with 2 of the others = 10, plus Y with 2 of the others = 10) also gives 30.
**Explain simply:**
- Order does not matter for a panel, so ABC and CBA are the same panel; that is why we divide by 3 x 2 x 1.
- "Cannot both" still allows X alone or Y alone; only the pair together is banned.
**Likely follow-ups:** *What if X and Y must both be on it?* Exactly 5 panels. *What if the panel has 4 people?* 35 total, forbidden = 5 choose 2 = 10, so 25 (verified by script).
**Common mistakes / traps:** Removing all panels that contain X or Y (that would be 35 - 20 = 15 wrong); counting ordered arrangements.

### Q30 ⭐⭐ 🔴 Mock Set 3, Q10 (suggested time 90 seconds): Mock Set 3 is the hardest set and you have 4 minutes left with 3 unattempted questions: a 4-clue syllogism (about 60 seconds for you), a 7-clue puzzle (about 4 minutes) and a one-step percentage question (about 45 seconds). There is negative marking. In what order do you proceed, what do you do with the puzzle, and why?
**Asked at:** commonly asked (no company-specific report found); time-management is a standard topic in prep-site advice (unverified).
**What the interviewer is checking:** Whether you choose by marks per minute and manage risk, not by order on the page.
**Say this in the interview:** "Percentage first (45 seconds), syllogism second (60 seconds), which is under 2 minutes for two likely marks. The puzzle needs my whole 4 minutes, so I only touch it with the leftover time, and I leave it blank unless I can cut the options down."
**Answer:** **Percentage question, then syllogism, then the puzzle only with the remaining time; if the puzzle is not finished, leave it or guess only after elimination.**
**Target time:** 90 seconds (as written in the heading).
**If you are short of time (our suggestion):** this is the short-of-time case; the rule is "cheapest marks first, long puzzle last, guess only if a wrong answer costs less than a right one gains".
**Step-by-step reasoning:**
1. Marks per minute: percentage 1 mark in 0.75 min; syllogism 1 mark in 1 min; puzzle 1 mark (or more) in 4 min.
2. Do the percentage first, then the syllogism: 45 + 60 = 105 seconds, leaving about 135 seconds.
3. The puzzle needs about 240 seconds, so it cannot be finished in 135 seconds at your usual speed. Use the leftover time to fill in what the first clues force, then look at the options.
4. Negative marking: a blind guess on a 5-option item with a 0.25 penalty has an expected value of 1/5 x 1 - 4/5 x 0.25 = 0 (break-even); on 4 options it is 1/4 - 3/4 x 0.25 = +0.0625. If you cannot rule out any option, leaving it blank is the safe choice; if you can rule out two or more, guessing has a positive expected value (hand-computed). The real penalty is not given here, so this is our suggestion.
**Fast method (30 seconds):** Rank questions by time needed, not by number; take the cheap ones first so an unlucky puzzle cannot eat them.
**Check:** Hand-checked: 45 + 60 = 105 seconds of 240; the expected values above are simple arithmetic.
**Explain simply:**
- "Expected value" is the average result if you repeated the same gamble many times.
- A guess is worth it only when the average gain beats the average loss.
- The puzzle can also be partly done: sometimes the first 3 clues already eliminate 3 of 5 options.
**Likely follow-ups:** *What if there were no negative marking?* Guess everything you cannot finish. *What if you had 6 minutes?* Still the cheap two first, then the puzzle with the remaining 3 minutes plus any time saved.
**Common mistakes / traps:** Starting the puzzle because it is "worth the same", then running out of time before the easy marks; guessing blind under heavy penalties.

### Q31 ⭐⭐⭐ 🟡 Mock Set 4, Q1 (suggested time 75 seconds): Statements: All bonds are assets. Some assets are risky. Conclusions: I. Some bonds are risky. II. No bond is risky. Which of the following is correct? (a) Only I follows (b) Only II follows (c) Either I or II follows (d) Neither follows (e) Both follow
**Asked at:** commonly asked (no company-specific report found); syllogisms are listed in prep-site reasoning topics (unverified).
**What the interviewer is checking:** Whether you test conclusions against every possible picture, not just one.
**Say this in the interview:** "The risky assets may or may not be the bonds. Both 'some bonds are risky' and 'no bond is risky' are possible, so neither is certain. But exactly one of them must be true, so the answer is (c) Either I or II follows."
**Answer:** **(c) Either I or II follows**
**Target time:** 75 seconds (as written in the heading).
**If you are short of time (our suggestion):** skip it only if the options are unfamiliar to you; with 5 options and no clear picture, a guess has no edge, so skip when there is a penalty.
**Step-by-step reasoning:**
1. Convention: each named group has at least one member; "some" means at least one.
2. Draw bonds fully inside assets. The "risky" circle must overlap assets, but it can sit in the part of assets outside bonds (then no bond is risky), or it can also reach into bonds (then some bonds are risky).
3. Both pictures obey the statements, so I is not forced and II is not forced.
4. I and II are opposites (one is the "some ... are" form, the other the "no ... is" form), so in every picture exactly one is true. When two conclusions are such a pair and neither alone follows, "either/or" is correct.
**Fast method (30 seconds):** Two conclusions that contradict each other, neither forced: choose "either-or" if the option exists.
**Check:** Verified by script: over every allowed region-occupancy of bonds, assets and risky, I is true in some models and false in others, II likewise, and exactly one of I, II is true in each model.
**Explain simply:**
- A conclusion "follows" only if it is true in every picture that fits the statements.
- "Either-or" applies when the two conclusions are a "some" and a "none" about the same two groups, and together they cover all cases.
**Likely follow-ups:** *Change statement 2 to "No asset is risky".* Then II follows definitely, so (b) Only II follows. *If there were a third conclusion "Some assets are bonds"?* It follows (all bonds are assets, bonds non-empty).
**Common mistakes / traps:** Picking (d) Neither because you only checked each alone; picking (a) from the word "some".

### Q32 ⭐⭐⭐ 🟡 Mock Set 4, Q2 (suggested time 60 seconds): Statement: R >= S = T < U. Conclusions: I. U > S. II. R >= T. III. R > U. Which conclusions definitely follow?
**Asked at:** commonly asked (no company-specific report found); inequality chains are a standard banking and service-MNC style item (unverified).
**What the interviewer is checking:** Reading a chain link by link and refusing to compare across a broken link.
**Say this in the interview:** "S equals T and T is below U, so U is above S: I is true. R is at least S and S equals T, so R is at least T: II is true. R and U are on opposite sides of S with no direct link, so III is not certain. Answer: I and II."
**Answer:** **Only I and II follow (III does not).**
**Target time:** 60 seconds (as written in the heading).
**If you are short of time (our suggestion):** do it; it is a quick mark. Check each conclusion in 10 seconds and move on.
**Step-by-step reasoning:**
1. Chain: R >= S, S = T, T < U.
2. I (U > S): S = T and T < U, so S < U, so U > S. True.
3. II (R >= T): R >= S and S = T, so R >= T. True.
4. III (R > U): R sits above S and U sits above S; nothing orders R against U. R could be bigger, equal or smaller.
**Fast method (30 seconds):** A conclusion is certain only if it follows by walking along the chain in one consistent direction; two things that both point "down to S" cannot be compared.
**Check:** Verified by script: over all small integer values, I and II are true in every case that fits, and III is true in some and false in others (for example R = 2, S = T = 2, U = 3 gives R < U).
**Explain simply:**
- ">=" means greater than or equal; "<" means strictly less.
- A definite conclusion must hold for every set of numbers that fits.
- A mix of "greater" and "less" on the two sides of a common point gives no ordering.
**Likely follow-ups:** *What if the chain were R >= S = T < U and the conclusion R >= U?* Still not certain, for the same reason. *What if it were R >= S = T and T >= U?* Then R >= U follows.
**Common mistakes / traps:** Marking III as true because R and U both seem "big"; thinking II needs strict inequality.

### Q33 ⭐⭐⭐ 🟡 Mock Set 4, Q3 (suggested time 90 seconds): M is the wife of N. N's mother is O. O's only daughter is P. P's husband is Q. How is Q related to M?
**Asked at:** commonly asked (no company-specific report found); blood-relation items are a standard reasoning topic (prep-site claim, unverified).
**What the interviewer is checking:** Whether you build the family step by step, with a small diagram, and get the generations right.
**Say this in the interview:** "N is O's child. O's only daughter is P, so N is not the daughter, N is a son. So P is N's sister, Q is her husband, and M is N's wife. Q is M's brother-in-law."
**Answer:** **Q is M's brother-in-law** (the husband of her husband's sister).
**Target time:** 90 seconds (as written in the heading).
**If you are short of time (our suggestion):** do it if you can sketch in 20 seconds; relation items are reliable marks. If the chain exceeds 4 links, skip.
**Step-by-step reasoning:**
1. Assumption (standard in these items): a wife is female and her husband is male, so N is male.
2. O is N's mother, so N is O's child. O's only daughter is P, and N is male, so N is O's son and P is N's sister.
3. Q is P's husband. M is N's wife.
4. Diagram:
   ```
   O (mother)
   ├── N (son)  = M (wife)
   └── P (daughter) = Q (husband)
   ```
5. M's husband N has a sister P, whose husband is Q. Q is M's husband's sister's husband: a brother-in-law (in-law by marriage on M's husband's side).
**Fast method (30 seconds):** Draw the two siblings under O, put each spouse beside them; the spouses of two siblings are linked as "in-laws" of each other.
**Check:** Hand-checked against every sentence; the only gender inference is N male from "wife of N" (and P female from "daughter").
**Explain simply:**
- A "brother-in-law" can be your spouse's brother, your sibling's husband, or your spouse's sister's husband. Here it is the last kind.
- "Only daughter" tells you the other child cannot be a daughter.
**Likely follow-ups:** *How is P related to M?* Sister-in-law (husband's sister). *How is O related to M?* Mother-in-law.
**Common mistakes / traps:** Calling Q "brother" or "husband's brother" (Q married into the family, he is not N's brother); forgetting that N must be a son.

### Q34 ⭐⭐⭐ 🟡 Mock Set 4, Q4 (suggested time 90 seconds): In a certain code, MARKET is written as NCUOJZ. Using the same rule, how is DEMAND written?
**Asked at:** commonly asked (no company-specific report found); letter-coding is listed among Mu Sigma style logical topics in a prep-site summary (unverified).
**What the interviewer is checking:** Spotting a shift that changes with the position of the letter.
**Say this in the interview:** "Comparing letter by letter, M to N is +1, A to C is +2, R to U is +3, K to O is +4, E to J is +5, T to Z is +6. Apply +1 to +6 to DEMAND and I get EGPESJ."
**Answer:** **EGPESJ**
**Target time:** 90 seconds (as written in the heading).
**If you are short of time (our suggestion):** do it; after the first two shifts (+1, +2) you can guess the pattern and check on the third letter in 20 seconds.
**Step-by-step reasoning:**
1. Letter positions: M13 to N14 (+1), A1 to C3 (+2), R18 to U21 (+3), K11 to O15 (+4), E5 to J10 (+5), T20 to Z26 (+6).
2. The k-th letter moves forward by k places.
3. DEMAND: D4+1 = 5 = E; E5+2 = 7 = G; M13+3 = 16 = P; A1+4 = 5 = E; N14+5 = 19 = S; D4+6 = 10 = J.
4. Result: E G P E S J.
**Fast method (30 seconds):** Write both words in numbers under each other and subtract; if the differences go 1, 2, 3, 4, 5, 6 you are done.
**Check:** Verified by script: the rule reproduces NCUOJZ from MARKET exactly and gives EGPESJ for DEMAND (no letter passes Z, so no wrap-around was needed).
**Explain simply:**
- A "shift" code moves each letter forward a fixed number of places; here the shift grows by 1 each position.
- After Z you would wrap to A.
**Likely follow-ups:** *Using the same rule, what is the code for ZEBRA?* Z+1 wraps to A, E+2 = G, B+3 = E, R+4 = V, A+5 = F: AGEVF (hand-checked).
**Common mistakes / traps:** Assuming a constant shift of +1 (M to N only fits the first letter); reading the code backwards.

### Q35 ⭐⭐ 🔴 Mock Set 4, Q5 (suggested time 120 seconds): Five departments HR, Legal, Finance, IT and Ops each occupy a different floor of a five-storey building (floors 1 to 5, floor 1 is the lowest). IT is on the top floor. HR and Legal are on adjacent floors, with Legal below HR. HR is not on floor 1. Finance is below Ops. Finance and IT are not on adjacent floors. Ops is exactly two floors above HR. Which department is on floor 3?
**Asked at:** commonly asked (no company-specific report found); linear arrangement puzzles are a standard reasoning item (prep-site claim, unverified).
**What the interviewer is checking:** Placing fixed facts first and using the strongest clue to pin the rest.
**Say this in the interview:** "IT is on 5. Ops is two above HR, and Ops cannot be on 5, so HR is on 1 or 2; HR is not on 1, so HR is on 2, Legal on 1, Ops on 4. Finance gets floor 3, which is below Ops and not next to IT. Floor 3 is Finance."
**Answer:** **Finance is on floor 3.**
**Target time:** 120 seconds (as written in the heading).
**If you are short of time (our suggestion):** this is a 5-item single-line puzzle with a clear start (IT on 5); do it in the first two thirds, skip only if you have already used your 2-minute puzzle budget.
**Step-by-step reasoning:**
1. IT is on floor 5.
2. Ops is two above HR; Ops cannot be on 5 (IT), so Ops is on 4 or lower, which puts HR on 1 or 2 (or 3 would give Ops 5, impossible).
3. HR is not on floor 1, so HR is on 2, and Ops is on 4.
4. Legal is directly below HR, so Legal is on 1.
5. Finance takes the last floor, 3. Check: Finance (3) is below Ops (4); Finance (3) and IT (5) are not adjacent.
6. Final arrangement:
   | Floor | 5 | 4 | 3 | 2 | 1 |
   |---|---|---|---|---|---|
   | Dept | IT | Ops | Finance | HR | Legal |
7. Unique: every other order breaks at least one clue (step 2 and 3 force HR on 2).
**Fast method (30 seconds):** Start from the clue with the most pinned facts ("Ops is exactly two above HR") combined with "IT is on the top"; the rest fills in.
**Check:** Verified by brute force over all 120 orderings: exactly one satisfies every clue.
**Explain simply:**
- "Adjacent" means directly next to; "exactly two floors above" means a gap of one floor in between.
- Every extra "not" clue (HR not on 1) is used to cut the remaining options.
**Likely follow-ups:** *Remove "HR is not on floor 1": is the answer still unique?* HR on 1 would put Ops on 3 and Legal below HR is impossible, so it stays unique (checked by reasoning; same final arrangement). *Which is on floor 4?* Ops.
**Common mistakes / traps:** Reading "Legal below HR" as "anywhere below"; forgetting that Ops cannot take floor 5.

### Q36 ⭐⭐ 🟡 Mock Set 4, Q6 (suggested time 75 seconds): A set of 10 coins looks identical, but one is heavier. Using only a two-pan balance with no weights, what is the minimum number of weighings that is guaranteed to find the heavy coin, and how do you show that fewer cannot work?
**Asked at:** commonly asked (no company-specific report found); weighing puzzles are a classic reasoning item.
**What the interviewer is checking:** Thinking in three outcomes per weighing (left heavy, right heavy, balance) and proving a lower bound.
**Say this in the interview:** "Each weighing has three outcomes, so two weighings can separate at most 9 cases. I have 10 coins, so two cannot always work. Three weighings are enough: 3 against 3, then narrow down. The answer is 3."
**Answer:** **3 weighings**
**Target time:** 75 seconds (as written in the heading).
**If you are short of time (our suggestion):** do it if you remember "three outcomes, powers of 3"; otherwise skip, as the lower-bound proof is the part that takes time.
**Step-by-step reasoning:**
1. Lower bound: a weighing ends in one of 3 ways (left pan down, right pan down, balance). After w weighings you can tell apart at most 3^w situations. There are 10 possible heavy coins. 3^2 = 9 < 10, so 2 weighings cannot always decide. 3^3 = 27 >= 10, so 3 might.
2. Method with 3: put 3 coins on each pan and keep 4 aside.
3. If a pan goes down, the heavy coin is among those 3: weigh 1 against 1; the heavier is it, or if they balance it is the third. Total 2 weighings.
4. If balanced, the heavy coin is among the 4: weigh 1 against 1; if one goes down it is that coin; if balanced it is one of the two remaining, weigh them (third weighing). Total 3 weighings in the worst case.
**Fast method (30 seconds):** Count: 3^1 = 3, 3^2 = 9, 3^3 = 27; the first power of 3 that is at least the number of coins is the number of weighings.
**Check:** Verified by script: smallest w with 3^w >= 10 is 3.
**Explain simply:**
- A "weighing" is one use of the balance; it gives left/right/equal, not a weight.
- Splitting into three groups (not two) uses all three outcomes.
- "Guaranteed" means worst case, not lucky case.
**Likely follow-ups:** *9 coins?* 2 weighings (3 vs 3, then 1 vs 1). *Up to how many coins in 4 weighings?* 81 (3^4).
**Common mistakes / traps:** Thinking in two outcomes only (heavier side or lighter side) and answering about 4 from the logarithm base 2 of 10; answering 2 because 9 is close to 10 (9 coins would need 2, 10 coins need 3).

### Q37 ⭐⭐ 🟡 Mock Set 4, Q7 (suggested time 75 seconds): A table orders has a column region with the values 'N', 'S', NULL, 'N', NULL (five rows). How many rows does SELECT * FROM orders WHERE region NOT IN ('N', NULL) return, and why?
**Asked at:** commonly asked (no company-specific report found); NULL traps in SQL are a common analyst interview topic.
**What the interviewer is checking:** Whether you know NULL is "unknown", and what that does inside NOT IN.
**Say this in the interview:** "Zero rows. NOT IN means 'not equal to N and not equal to NULL'. Comparing anything to NULL gives unknown, so the whole condition can never be true. Even 'S' is dropped."
**Answer:** **0 rows**
**Target time:** 75 seconds (as written in the heading).
**If you are short of time (our suggestion):** this is a one-line logic item, so do it early; the rule is "NOT IN with a NULL in the list returns nothing".
**Step-by-step reasoning:**
1. `region NOT IN ('N', NULL)` is the same as `region <> 'N' AND region <> NULL`.
2. `x <> NULL` is neither true nor false but UNKNOWN. SQL keeps a row only when the condition is TRUE.
3. Row 'N': first part false, so the AND is false. Row 'S': first part true, second UNKNOWN, TRUE AND UNKNOWN = UNKNOWN, so the row is dropped. NULL rows: UNKNOWN, dropped.
4. Real output from Python's sqlite3 (run here):
   ```
   SELECT * FROM orders WHERE region NOT IN ('N', NULL);   -> [] (0 rows)
   SELECT * FROM orders WHERE region NOT IN ('N');          -> [('S',)] (1 row)
   SELECT * FROM orders WHERE region NOT IN ('N') OR region IS NULL;  -> [('S',), (None,), (None,)] (3 rows)
   ```
5. This three-valued logic is standard SQL; other databases (PostgreSQL, SQL Server, Oracle) follow it too, from memory, not run here; confirm in the tool.
**Check:** Verified by script on sqlite3 as shown above.
**Explain simply:**
- NULL means "unknown value", not "empty text" and not zero.
- A WHERE keeps only rows where the test is TRUE; UNKNOWN is thrown away like FALSE.
- Use `IS NULL` / `IS NOT NULL` to test for NULL, never `= NULL`.
**Likely follow-ups:** *Remove NULL from the list:* `NOT IN ('N')` returns 1 row ('S'); NULL-region rows still do not appear. *How to keep the NULL rows too?* Add `OR region IS NULL` (3 rows, verified).
**Common mistakes / traps:** Answering 1 ('S') or 3 ('S' plus the NULLs); thinking NULL <> 'N' is true.

### Q38 ⭐⭐ 🟡 Mock Set 4, Q8 (suggested time 75 seconds): Without a calculator, how can you compute 98 x 52 exactly in one line, and what is the result?
**Asked at:** commonly asked (no company-specific report found); mental-arithmetic shortcuts are standard in aptitude gates.
**What the interviewer is checking:** Using a near-round number and the distributive rule instead of long multiplication.
**Say this in the interview:** "98 is 100 minus 2, so 98 x 52 is 100 x 52 minus 2 x 52, which is 5200 minus 104, so 5096."
**Answer:** **5096**
**Target time:** 75 seconds (as written in the heading).
**If you are short of time (our suggestion):** do it; it takes 20 seconds. Never skip a near-round multiplication.
**Step-by-step reasoning:**
1. Rewrite 98 as 100 - 2.
2. (100 - 2) x 52 = 100 x 52 - 2 x 52 (the distributive rule: multiplying a difference means multiplying each part).
3. 5200 - 104 = 5096.
**Fast method (30 seconds):** Anchor on the nearest round number (100) and correct by the small gap (2 times the other number).
**Check:** Verified by script: 98 x 52 = 5096.
**Explain simply:**
- "Distributive rule": a x (b - c) = a x b - a x c.
- It works for any number near 10, 100, 1000.
**Likely follow-ups:** *99 x 47?* 4700 - 47 = 4653 (hand-checked). *102 x 52?* 5200 + 104 = 5304.
**Common mistakes / traps:** Subtracting 2 instead of 2 x 52; arithmetic slip in 5200 - 104 (answering 5106).

### Q39 ⭐⭐ 🟡 Mock Set 4, Q9 (suggested time 75 seconds): "Team A closed 20% more tickets than Team B last month, so Team A is more productive." Which unstated assumption does this argument most need?
Options: (a) Both teams handled tickets of comparable volume and complexity. (b) Team A has more members than Team B. (c) Team B's manager is stricter. (d) Closed tickets have been the only productivity measure used so far.
**Asked at:** commonly asked (no company-specific report found); assumption-finding is a standard critical-reasoning item.
**What the interviewer is checking:** Whether you spot that a raw count is not a fair comparison and name the gap in the argument.
**Say this in the interview:** "The argument jumps from 'more tickets closed' to 'more productive'. That only holds if the tickets are comparable in difficulty and the teams had a similar workload. That is (a)."
**Answer:** **(a)**
**Target time:** 75 seconds (as written in the heading).
**If you are short of time (our suggestion):** do it; for "which assumption" items, pick the option that, if false, would break the argument, and move on.
**Step-by-step reasoning:**
1. Conclusion: A is more productive. Evidence: A closed 20% more tickets.
2. Gap: if A got easier or more tickets, closing more says nothing about productivity. The argument needs comparable volume and complexity.
3. Negation test (if the assumption were false, the argument collapses): if Team B's tickets were much harder, the evidence no longer supports the conclusion. This works for (a).
4. Why the others fail: (b) is the opposite direction; more members would make A's count less impressive per person, so the argument would need that to be false, not true. (c) Manager strictness is irrelevant. (d) The argument does not need other measures to be absent; even if other measures exist, it is claiming productivity from this one.
**Fast method (30 seconds):** Ask "what would make this evidence meaningless?" The answer is the assumption.
**Check:** Hand-checked with the negation test on each option.
**Explain simply:**
- An "assumption" is an unstated step the conclusion depends on.
- Raw counts need a fair base: per person, per hour or per equal difficulty.
**Likely follow-ups:** *What data would test it?* Tickets per person, and a mix by complexity. *What if Team A were twice as large?* Then A's per-person output would be lower; the 20% gap would not show higher productivity.
**Common mistakes / traps:** Choosing (b) (it actually weakens the claim); choosing (d) because it sounds like a "measure" statement.

### Q40 ⭐⭐ 🟡 Mock Set 4, Q10 (suggested time 75 seconds): A mock set of 10 questions scores +1 for a correct answer and -0.25 for a wrong one. You attempt 9 questions and get 7 right. What are your net score and your accuracy on attempted questions, and what do the two numbers tell you to improve first?
**Asked at:** commonly asked (no company-specific report found); score-review habits belong to Part 1 of this book (our suggestion).
**What the interviewer is checking:** Whether you can compute a net score and separate accuracy from coverage.
**Say this in the interview:** "7 right gives 7; 2 wrong costs 0.5, so my net is 6.5 out of 10. Accuracy on attempted is 7 out of 9, about 77.8%. I would improve accuracy on the wrong ones first."
**Answer:** **Net score 6.5 out of 10; accuracy 7/9, about 77.8% (rounded to one decimal).**
**Target time:** 75 seconds (as written in the heading).
**If you are short of time (our suggestion):** do it; it is 20 seconds of arithmetic. Compute net first, accuracy second.
**Step-by-step reasoning:**
1. Wrong answers = 9 - 7 = 2.
2. Net = 7 x 1 - 2 x 0.25 = 7 - 0.5 = 6.5.
3. Accuracy on attempted = 7 / 9 = 0.7778, about 77.8%.
4. One question was left blank, and the maximum possible was 10.
5. What to improve (our suggestion): a wrong answer costs you 1.25 marks compared with getting it right (+1 instead of -0.25), while the blank cost at most 1. So first look at why the two wrong answers happened (misread, careless, concept gap). Then, if the blank was from slowness, work on speed. A single set is a small sample, so treat the pattern across several mocks as the signal.
**Fast method (30 seconds):** Net = right minus (wrong x penalty); accuracy = right divided by attempted (not by all questions).
**Check:** Verified by script: 6.5 and 77.8%.
**Explain simply:**
- "Accuracy on attempted" ignores blanks; "net score" counts everything.
- If accuracy is high but net is low, you are not attempting enough; if attempts are high and accuracy is low, the penalty is eating your score.
**Likely follow-ups:** *Net if you guessed the blank and got it wrong?* 7 - 3 x 0.25 = 6.25. *If right?* 8 - 0.5 = 7.5, accuracy 8/10 = 80% (hand-checked).
**Common mistakes / traps:** Dividing 7 by 10 for accuracy (70%); forgetting the penalty; treating accuracy as the only number.

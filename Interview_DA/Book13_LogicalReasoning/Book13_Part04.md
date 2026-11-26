# Book 13 — Logical Reasoning & Analytical Thinking | Part 4: Seating, Floor, Box, Month and Day Arrangements 🟡🔴

**Target:** 70 questions | **Actual:** 74 questions
**Scope:** linear and circular seating (including mixed facing, two parallel rows and alternating groups), rectangular-table, floor, stacked-box, weekday-schedule and month arrangements, circular roster and date-pattern puzzles, counting seatings, plus method and trap questions; every puzzle states all clues and has a single checkable answer.

### Q1 ⭐⭐⭐ 🟢 5 interns Asha, Bala, Chitra, Dev and Esha live in a 5-floor building, one person per floor, floors numbered 1 (lowest) to 5 (top). (1) Esha lives on an even-numbered floor. (2) Chitra lives 2 floors above Esha. (3) Dev lives on a lower floor than Chitra. (4) Asha lives on neither the top floor nor floor 1. Who lives immediately above Chitra?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Can you turn "above/below" and "even floor" clues into fixed numbers one at a time.
**Say this in the interview:** "Esha must be on floor 2 or 4, but Chitra is 2 above her, so Esha is on 2 and Chitra on 4. Dev is below Chitra, Asha is not on 1 or 5, so Bala gets 5. Bala lives immediately above Chitra."
**Answer:** **Bala** (floor 5, directly above Chitra on floor 4).
**Step-by-step reasoning:**
1. Esha is on an even floor: 2 or 4.
2. Chitra is Esha + 2. If Esha were on 4, Chitra would be on 6, which does not exist. So Esha = 2, Chitra = 4.
3. Dev is below Chitra, so Dev is on 1 or 3 (floor 2 is Esha's).
4. Asha is not on 1 or 5, so Asha is on 3 (the only free middle floor). Then Dev = 1 and Bala = 5.

| Floor | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|
| Person | Bala | Chitra | Asha | Esha | Dev |

Unique: every step above was forced; a brute force over all 120 orders found exactly this one.
**Fast method (30 seconds):** Start with the clue that has the fewest options (even floor plus "2 above" leaves one choice because floor 6 is missing). Then fill the "not on" clue last.
**Check:** Esha 2 is even; Chitra 4 = 2 + 2; Dev 1 < 4; Asha 3 is not 1 or 5. All four clues hold.
**Explain simply:**
- "Immediately above" means the next floor number up.
- Edge floors (top and bottom) limit options: a person "2 above" someone cannot be on a floor beyond the top.
**Likely follow-ups:** 1) *Drop clue (4); is the answer still fixed?* No; brute force gives 4 arrangements, and in two of them Asha (not Bala) is on floor 5, so the answer would change. Clue (4) is what makes it unique. 2) *Who lives on floor 1?* Dev.
**Common mistakes / traps:** Forgetting that floor 6 does not exist, so you keep Esha on 4; or reading "2 floors above" as "next but one person" without checking the building height.

### Q2 ⭐⭐⭐ 🟡 6 colleagues Asha, Bala, Chitra, Dev, Esha and Farid sit in a row facing north (so each person's right-hand side is towards the east). (1) Dev sits third to the right of Asha. (2) Chitra sits immediately between Asha and Farid. (3) Farid sits somewhere to the left of Bala. (4) Esha sits at the extreme left end. Who sits immediately to the right of Farid?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Anchoring the one fixed seat and chaining relative clues along a row.
**Say this in the interview:** "Esha is at the left end, position 1. Dev is three seats right of Asha and Chitra sits between Asha and Farid. That only works with Asha in 2, Chitra 3, Farid 4, Dev 5, leaving Bala 6. Dev sits immediately right of Farid."
**Answer:** **Dev**.
**Step-by-step reasoning:**
1. Number seats 1 to 6 from the left (west) end. Esha = 1.
2. Dev is 3 seats right of Asha, so (Asha, Dev) can be (2,5) or (3,6) (Esha holds 1).
3. Chitra is directly between Asha and Farid, so Asha, Chitra, Farid are three seats in a row. Farid is left of Bala.
4. Test Asha = 3 (so Dev = 6). Chitra is then in seat 2 or 4. Seat 2 puts Farid in seat 1, which is Esha's. Seat 4 puts Farid in seat 5, and Bala (right of Farid) would need seat 6, which is Dev's. So Asha = 3 fails and Asha = 2.
5. Asha = 2, Dev = 5. Chitra between Asha and Farid: Chitra = 3, Farid = 4 (Chitra = 1 is Esha's). Bala = 6.

| Seat | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Person | Esha | Asha | Chitra | Farid | Dev | Bala |

Unique by brute force over all 720 orders.
**Fast method (30 seconds):** Place the fixed-seat clue first, then build the "block" (Asha, Chitra, Farid) as one unit of three seats, and slide it until the other clues fit.
**Check:** Dev (5) = Asha (2) + 3; Chitra (3) is between 2 and 4; Farid 4 < Bala 6; Esha is seat 1. All hold.
**Explain simply:**
- "Facing north, right is east", so "to the right" means a higher seat number when you number from the left end of the page.
- "Third to the right of Asha" means 3 seats along, so the gap is 3 (two people in between).
**Likely follow-ups:** 1) *Drop clue (4); still unique?* No; brute force gives 5 arrangements, so the left-end clue is essential. 2) *Who sits second to the left of Dev?* Chitra.
**Common mistakes / traps:** Treating "third to the right" as "three people between"; it is two between. Also forgetting that "between Asha and Farid" can run either way round, which is why a block is tried both ways.

### Q3 ⭐⭐⭐ 🟡 7 interview-panel members A, B, C, D, E, F and G sit in a row facing north (so each person's right-hand side is towards the east). (1) D sits immediately to the right of B. (2) G sits immediately to the right of E. (3) B and G do not sit next to each other. (4) F sits immediately to the right of C. (5) Exactly 2 persons sit between C and E. (6) A sits third from the left end. Who sits second to the right of E?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Handling several pair clues, a "not adjacent" clue and a gap clue in a 7-seat row.
**Say this in the interview:** "I glue the pairs: B-D, E-G and C-F. A is in seat 3. C and E have exactly two people between them. Trying the options, only E G A C F B D works. Second to the right of E is A."
**Answer:** **A**.
**Step-by-step reasoning:**
1. Number seats 1 to 7 from the left. Pairs (left then right): B D, E G, C F. A = seat 3.
2. That leaves three pairs plus A. Pairs take 2 seats each (6 seats), A takes seat 3, so A splits the row: seats 1-2 hold one pair, and seats 4-7 hold two pairs.
3. Condition (5): exactly 2 people between C and E, so seats differ by 3. Try E G in seats 1-2: E = 1, so C = 4 (then F = 5, and B D takes 6-7). Check (3): B = 6 and G = 2 are not adjacent. Works.
4. Other tries fail: if C F is in seats 1-2 then C = 1 and E = 4, giving E G = 4-5 and B D = 6-7, but G (5) and B (6) are adjacent, breaking (3). If B D is in seats 1-2 then C and E in 4-7 cannot differ by 3 with pairs of width 2 (C F and E G occupy 4-5 and 6-7, a difference of 2 only).

| Seat | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Person | E | G | A | C | F | B | D |

Unique by brute force over all 5040 orders.
**Fast method (30 seconds):** Treat "immediately right of" pairs as 2-seat blocks, then see where the fixed seat (A) and the one gap clue let the blocks fit.
**Check:** D right of B; G right of E; B (6) and G (2) apart; F right of C; C (4) and E (1) have 2 between them (G, A); A is third from left. All hold.
**Explain simply:**
- A "block" is two people who must stay together, handled as one object.
- "Exactly 2 between" means the seat numbers differ by 3.
**Likely follow-ups:** 1) *Who sits second to the left of D?* D is seat 7, so second left is seat 5, F. 2) *Who is immediately left of B?* F.
**Common mistakes / traps:** Skipping the "not next to each other" clue, which is what kills the E-G in seats 4-5 option; and counting "2 between" as a difference of 2.

### Q4 ⭐⭐⭐ 🟡 7 payroll clerks A, B, C, D, E, F and G sit in a row facing north (so each person's right-hand side is towards the east). (1) E sits immediately to the right of A. (2) F sits immediately to the right of C. (3) Exactly 3 persons sit between A and D. (4) G sits somewhere to the left of A. (5) Exactly 1 person sits between A and G. How many persons sit between B and C?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Using gap clues ("exactly n between") and left/right to pin down a row, then answering a counting question.
**Say this in the interview:** "A and G have exactly one person between them with G on the left, so G A are two apart. D is four seats from A. With E right after A and C F as a pair, the row is G B A E C F D. Between B and C there are two people."
**Answer:** **2** (A and E sit between B and C).
**Step-by-step reasoning:**
1. Number seats 1 to 7 from the left. G is left of A with exactly 1 person between: G = A - 2.
2. E is immediately right of A, so E = A + 1. D has 3 between with A, so D = A + 4 or A - 4.
3. Try A = 3: G = 1, E = 4, D = 7 (A - 4 would be negative). Remaining seats 2, 5, 6 for B, C, F. C F must be adjacent: seats 5 and 6. So B = 2.
4. Other A values fail: A = 4 puts G = 2, E = 5, D = 8 or 0, impossible; A = 5 gives D = 1, G = 3, E = 6, leaving seats 2, 4, 7 with no adjacent pair for C F; A = 6 gives E = 7, D = 2, G = 4, leaving 1, 3, 5, no adjacent pair; A = 2 has no seat for G.

| Seat | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Person | G | B | A | E | C | F | D |

Unique by brute force over all 5040 orders. B is seat 2, C is seat 5, so the people between are seats 3 and 4: A and E.
**Fast method (30 seconds):** Put A and its tied people (G, E) in a small block "G _ A E", slide it along the row, and test the D gap and the C F pair.
**Check:** E right of A; F right of C; A (3) and D (7) have 3 between (E, C, F in seats 4, 5, 6); G left of A; one person (B) between G and A. All hold.
**Explain simply:**
- "Exactly 3 between" means a seat difference of 4.
- "Somewhere to the left" only means a smaller seat number, not next to.
**Likely follow-ups:** 1) *Who is third to the right of G?* E... G is seat 1, so seat 4, E. 2) *How many sit between D and G?* 5.
**Common mistakes / traps:** Counting seats instead of people in between (off by one); and forgetting D could be on either side of A (here only one side fits).

### Q5 ⭐⭐⭐ 🟡 6 auditors A, B, C, D, E and F sit in a row facing north (so each person's right-hand side is towards the east). (1) A and B do not sit next to each other. (2) A sits third to the right of F. (3) D sits somewhere to the left of F. (4) Exactly 3 persons sit between B and C. Who sits second to the right of F?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Combining a gap clue (3 between) with a "not next to" clue in a short row.
**Say this in the interview:** "Exactly 3 between B and C means they are at the two ends. A is third right of F, D is left of F, and A and B are not neighbours. That gives B D F E C A. Second to the right of F is C."
**Answer:** **C**.
**Step-by-step reasoning:**
1. Six seats, 3 people between B and C means their seat numbers differ by 4, so the pair of seats is (1,5) or (2,6), in either order.
2. So (B,C) = (1,5), (5,1), (2,6) or (6,2). A is 3 seats right of F; D is left of F.
3. Try B = 1, C = 5: F must have D to its left and A three right of it, so F = 3, A = 6, D = 2, E = 4. Check (1): A (6) and B (1) are not next to each other. Works.
4. The other three placements fail: C = 1, B = 5 forces F = 3 and A = 6, so A and B are neighbours (breaks clue 1); with B and C in seats 2 and 6 no seat for F has D to its left and A three seats to its right without clashing with B or C.

| Seat | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Person | B | D | F | E | C | A |

Unique by brute force over all 720 orders.
**Fast method (30 seconds):** Do the biggest gap clue first; it leaves only four placements. Then F's two clues (D to its left, A three to its right) fix F quickly.
**Check:** A and B (6 and 1) not adjacent; A = F + 3; D (2) < F (3); between B (1) and C (5) are D, F, E (3 people). All hold.
**Explain simply:**
- "Exactly 3 persons between" means the seat numbers differ by 4, not 3.
- A negative clue ("do not sit next to") is used to remove options, not to place anyone.
**Likely follow-ups:** 1) *Who sits immediately to the left of E?* F. 2) *Remove clue (1); is it still unique?* No; brute force gives 2 arrangements (B D F E C A and C D F E B A), so clue (1) is needed to separate them.
**Common mistakes / traps:** Reading "3 persons between" as a gap of 3 seats (difference 3) rather than difference 4, which gives wrong placements.

### Q6 ⭐⭐⭐ 🟡 7 panel members Asha, Bala, Chitra, Dev, Esha, Farid and Gita sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) Bala sits immediately to the right of Gita. (2) Farid sits third to the right of Gita. (3) Asha and Esha are not neighbours. (4) Esha sits immediately to the right of Farid. (5) Chitra and Gita are neighbours. Who sits second to the left of Gita?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Converting circular "right/left" into steps around the table without losing direction.
**Say this in the interview:** "Everyone faces the centre, so right means anticlockwise. I number the seats anticlockwise starting at Gita as 0. Bala is 1, Farid is 3, Esha is 4. Chitra must be next to Gita, so seat 6. Asha and Esha must not be neighbours, so Asha is seat 2 and Dev is 5. Second to the left of Gita is seat 5: Dev."
**Answer:** **Dev**.
**Step-by-step reasoning:**
1. Convention: facing the centre, a person's right is anticlockwise. Number seats 0 to 6 anticlockwise; Gita = 0.
2. Bala is immediately right of Gita: seat 1. Farid is third right: seat 3. Esha is immediately right of Farid: seat 4.
3. Chitra is a neighbour of Gita: seat 1 (taken) or seat 6, so seat 6.
4. Seats 2 and 5 remain for Asha and Dev. Seat 5 is next to Esha (4), so Asha cannot be there. Asha = 2, Dev = 5.
5. Second to the left of Gita is 2 steps clockwise: seat 0 - 2 = seat 5 (mod 7), Dev.

Anticlockwise order: Gita, Bala, Asha, Farid, Esha, Dev, Chitra (then back to Gita).
Unique up to turning the whole table (Gita is fixed at 0); checked by brute force over all 720 fillings.
**Fast method (30 seconds):** Fix the most-mentioned person (Gita) as seat 0, write seat numbers 0 to 6, and add "k to the right = plus k, k to the left = minus k, wrap around at 7".
**Check:** Bala 1 = 0 + 1; Farid 3 = 0 + 3; Esha 4 = 3 + 1; Chitra 6 is next to 0; Asha 2 and Esha 4 are not neighbours. All hold.
**Explain simply:**
- A circle has no start, so we pick one person and call that seat 0; the answer does not depend on which seat is 0.
- "Mod 7" just means "wrap round after seat 6 back to 0".
**Likely follow-ups:** 1) *If everyone instead faced outward, who is immediately right of Gita?* Right then becomes clockwise, so seat 6, Chitra. 2) *Who is between Asha and Esha?* Farid.
**Common mistakes / traps:** Using clockwise as "right" (the most common circular error); and forgetting to wrap around.

### Q7 ⭐⭐⭐ 🟡 7 colleagues A, B, C, D, E, F and G sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) B sits third to the right of E. (2) C sits immediately to the right of B. (3) A sits immediately to the left of B. (4) E sits immediately between F and G. (5) E sits immediately to the right of G. Who sits second to the right of B?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Placing a connected group on a circle and handling a clue that names both neighbours.
**Say this in the interview:** "Facing the centre, right is anticlockwise. G, E, F sit consecutively with E in the middle and E right of G. B is third right of E; C is right of B and A is left of B. That gives E F A B C D G going anticlockwise. Second right of B is D."
**Answer:** **D**.
**Step-by-step reasoning:**
1. Number seats 0 to 6 anticlockwise (the "right" direction), with E = 0.
2. E is immediately between F and G, and E is right of G, so G = 6 (one step clockwise from E) and F = 1.
3. B is third right of E: B = 3.
4. C is immediately right of B: C = 4. A is immediately left of B: A = 2.
5. The last person D takes seat 5. Second right of B is seat 5, D.

Anticlockwise order: E, F, A, B, C, D, G.
Unique up to rotation; brute force over all 720 fillings found one.
**Fast method (30 seconds):** Start with the 3-person cluster (G E F) since it has the most clues, then add the others by plus/minus steps.
**Check:** B (3) = E (0) + 3; C (4) right of B; A (2) left of B; E between F (1) and G (6), E right of G. All hold.
**Explain simply:**
- Right means plus (anticlockwise); left means minus (clockwise).
- "Immediately between" a pair says the two neighbours but not which is on which side; the clue "E right of G" decides that.
**Likely follow-ups:** 1) *Who is third to the left of A?* G (seat 2 - 3 = 6). 2) *If "E immediately right of G" were removed, could F and G swap?* Then the swapped table would also fit clues 1-4; that is why clue 5 exists.
**Common mistakes / traps:** Reading "between F and G" as fixing the side; and confusing "A immediately left of B" with "A right of B".

### Q8 ⭐⭐⭐ 🟡 6 employees Asha, Bala, Chitra, Dev, Esha and Farid live in a 6-floor building, one person per floor, floors numbered 1 (lowest) to 6 (top). (1) Exactly 1 floor lies between the floors of Asha and Esha. (2) Chitra lives 2 floors above Esha. (3) Esha lives on the floor immediately between those of Dev and Farid. (4) Esha lives on an odd-numbered floor. (5) Esha lives on a lower floor than Dev. How many floors lie between the floors of Bala and Esha?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Building a vertical order from gap clues and a parity clue (odd floor).
**Say this in the interview:** "Esha is on an odd floor and sits between Dev and Farid with Dev above her. Chitra is 2 above Esha and Asha is 2 from Esha. Only Esha = 3 works: Farid 2, Dev 4, Chitra 5, Asha 1, Bala 6. Between Bala and Esha are floors 4 and 5, so 2."
**Answer:** **2** (Dev and Chitra).
**Step-by-step reasoning:**
1. Esha is odd: floor 1, 3 or 5. She needs a neighbour on each side, so not floor 1: floor 3 or 5. Chitra is 2 above her, so floor 5 is impossible (floor 7 does not exist). Esha = 3, Chitra = 5.
2. Esha is between Dev and Farid, with Dev above: Dev = 4, Farid = 2.
3. Asha is exactly 1 floor away (a difference of 2) from Esha: floor 1 or 5; floor 5 is Chitra's, so Asha = 1. Bala = 6.

| Floor | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|
| Person | Bala | Chitra | Dev | Esha | Farid | Asha |

Unique by brute force over all 720 arrangements.
**Fast method (30 seconds):** Use the clue that ties Esha to the building edges: "between two people" removes the end floors, and "Chitra 2 above" removes floor 5.
**Check:** Asha 1 and Esha 3: one floor between; Chitra 5 = 3 + 2; Esha 3 between Farid 2 and Dev 4; Esha 3 is odd; Esha below Dev. All hold.
**Explain simply:**
- "Exactly 1 floor between" means the floor numbers differ by 2.
- Count people between by listing the floors strictly between them.
**Likely follow-ups:** 1) *Who lives immediately above Dev?* Chitra. 2) *If clue (4) said an even floor instead?* Verified by script: still unique, bottom to top Bala, Asha, Farid, Esha, Dev, Chitra, and the answer is still 2.
**Common mistakes / traps:** Counting both end floors in the "between" answer (that gives 4), or forgetting that "between Dev and Farid" does not say which is above, so clue (5) is needed.

### Q9 ⭐⭐⭐ 🟡 6 managers Asha, Bala, Chitra, Dev, Esha and Farid live in a 6-floor building, one person per floor, floors numbered 1 (lowest) to 6 (top). (1) Asha lives on a lower floor than Farid. (2) Farid lives immediately above Dev. (3) Exactly 1 floor lies between the floors of Chitra and Esha. (4) Bala lives immediately above Chitra. (5) Chitra lives on a lower floor than Asha. How many floors lie between the floors of Bala and Dev?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Chaining "immediately above" links into stacked blocks, then fitting a gap clue.
**Say this in the interview:** "Bala is right above Chitra and Farid is right above Dev, so those are two 2-floor blocks. Chitra is below Asha and Asha is below Farid, which with a one-floor gap for Chitra and Esha gives Chitra 1, Bala 2, Esha 3, Asha 4, Dev 5, Farid 6. Between Bala and Dev are Esha and Asha, so 2."
**Answer:** **2** (Esha and Asha).
**Step-by-step reasoning:**
1. Clues 2 and 4 make two blocks (bottom then top): Chitra, Bala and Dev, Farid.
2. Asha is above Chitra and below Farid. Asha is not Bala or Dev, so she sits above Bala and below Dev. Order so far: Chitra, Bala, Asha, Dev, Farid.
3. Esha must slot into that order with exactly 1 floor between her and Chitra. Slots: below Chitra (difference 1), between Bala and Asha (difference 2, works), between Asha and Dev (difference 3), above Farid (difference 5). Only the second slot works.
4. Floors: Chitra 1, Bala 2, Esha 3, Asha 4, Dev 5, Farid 6.

| Floor | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|
| Person | Farid | Dev | Asha | Esha | Bala | Chitra |

Unique by brute force over all 720 arrangements.
**Fast method (30 seconds):** Merge every "immediately above" into a block first; the puzzle shrinks from 6 people to 3 or 4 units.
**Check:** Asha 4 < Farid 6; Farid 6 is right above Dev 5; Chitra 1 and Esha 3 have one floor between; Bala 2 right above Chitra; Chitra 1 < Asha 4. All hold.
**Explain simply:**
- A block is two people forced to be neighbours; treat it as one thing, then place the blocks.
- "Lower floor than" does not need the floors to be next to each other.
**Likely follow-ups:** 1) *Who lives on floor 4?* Asha. 2) *Who lives on floor 5?* Dev.
**Common mistakes / traps:** Treating "lower floor" as "directly below", and counting Bala or Dev themselves in the "between" total.

### Q10 ⭐⭐⭐ 🟡 5 training sessions Excel, SQL, Python, Power BI and Statistics are each scheduled on a different day of 5 consecutive days starting Monday, one per day. (1) Excel comes earlier in the schedule than Power BI. (2) SQL is the day after Python. (3) Excel is the day after SQL. (4) Exactly 2 days separate SQL and Power BI. On which day is Statistics?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles appear in prep-site topic lists for TCS NQT, Infosys, Wipro, Cognizant and Mu Sigma (single-site claims, unverified).
**What the interviewer is checking:** Ordering events in a schedule using "day after" and "gap" clues.
**Say this in the interview:** "SQL is the day after Python, and Excel is the day after SQL, so the chain is Python, SQL, Excel on three days in a row. Power BI is 3 days from SQL and after Excel, so it is on Friday, and Statistics fills the remaining slot: Thursday."
**Answer:** **Thursday**.
**Step-by-step reasoning:**
1. Chain: Python, then SQL, then Excel, on consecutive days.
2. "Exactly 2 days separate SQL and Power BI" means they are 3 days apart. Power BI is after Excel (clue 1), so after SQL: Power BI = SQL + 3.
3. If the chain starts Monday: Python Mon, SQL Tue, Excel Wed, Power BI Fri. Statistics takes Thursday.
4. If the chain started Tuesday, SQL = Wed and Power BI = Sat, which is outside the 5 days. So Monday is the only start.

| Day | Mon | Tue | Wed | Thu | Fri |
|---|---|---|---|---|---|
| Session | Python | SQL | Excel | Statistics | Power BI |

Unique by brute force over all 120 orders.
**Fast method (30 seconds):** Write the consecutive chain first, then use the end of the week (5 days) to see where the gap clue can still fit.
**Check:** Excel (Wed) before Power BI (Fri); SQL (Tue) is the day after Python (Mon); Excel is the day after SQL; Tue and Fri have Wed and Thu between them (2 days). All hold.
**Explain simply:**
- "Exactly 2 days separate" means a difference of 3 days (the 2 in between, plus one more step).
- Schedules are the same as floors: a line of numbered slots.
**Likely follow-ups:** 1) *If Excel were later than Power BI?* Verified by script: Power BI Mon, Statistics Tue, Python Wed, SQL Thu, Excel Fri, so Statistics falls on Tuesday. 2) *Which day is SQL?* Tuesday.
**Common mistakes / traps:** Reading "2 days separate" as a difference of 2 (it gives Thursday for Power BI, wrong).

### Q11 ⭐⭐⭐ 🟡 In a linear seating puzzle, how do you decide which person is on whose left or right when the people face north in one row and south in another, and how do you keep both rows consistent in one diagram?
**Asked at:** commonly asked (no company-specific report found); two-row seating appears in prep-site topic lists (unverified).
**What the interviewer is checking:** Whether you know that "right" depends on which way the person faces, and can keep one fixed compass.
**Say this in the interview:** "I fix the compass on the page first: west on the left, east on the right. For people facing north, their left is west and their right is east. For people facing south, it flips: their right is west and their left is east. I never use my own left and right."
**Answer:** **Anchor everything to compass directions on the page; convert each person's "left/right" using the way they face.**
**Step-by-step reasoning:**
1. Draw the two rows as parallel lines, north row on top (facing south) and south row below (facing north) unless the puzzle says otherwise. Mark W on the left of the page and E on the right.
2. North-facing person: left = West = left of page; right = East = right of page.
3. South-facing person: left = East = right of page; right = West = left of page.
4. Convert every clue straight to W or E before drawing, then place people by page position.
5. Use "opposite" or "facing" clues to line the two rows up as columns.

Worked mini-example: row 1 faces north, row 2 faces south. "P (row 1) sits immediately to the right of Q": P is just east of Q on the page. "R (row 2) sits immediately to the right of S": R is just west of S on the page, the opposite side.
**Explain simply:**
- Your left and right change when you turn around; north and south on the page do not.
- Two people facing each other have opposite left and right, so the same word points to opposite page sides.
**Likely follow-ups:** 1) *What if both rows face the same way?* Then left and right agree for both rows. 2) *What if rows face each other and the puzzle gives "east" directly?* Use it without conversion.
**Common mistakes / traps:** Reading left and right off the page for the row that faces south; the commonest wrong turn in two-row puzzles.

### Q12 ⭐⭐⭐ 🟡 In a circular seating puzzle where everyone faces the centre, how do you turn "second to the right of X" into a seat number, and what changes when a person faces outside the circle?
**Asked at:** commonly asked (no company-specific report found); circular tables facing the centre are a standard format on prep sites (unverified).
**What the interviewer is checking:** Whether you have a mechanical rule for "to the right" and "to the left" on a circle, including the outward-facing case.
**Say this in the interview:** "Facing the centre, right is anticlockwise. I number seats anticlockwise from 0 and write right as plus and left as minus, wrapping around. If someone faces outward, their right flips to clockwise, so the sign flips for that person."
**Answer:** **Facing the centre: k-th to the right of seat s is seat (s + k) mod n and k-th to the left is (s - k) mod n, with seats numbered anticlockwise. Facing outside: right becomes clockwise, so the signs swap for that person.**
**Step-by-step reasoning:**
1. Pick a reference person as seat 0 and number seats 0 to n-1 anticlockwise.
2. For n = 7: "second to the right of seat 0" is seat 2; "third to the left of seat 0" is (0 - 3) mod 7 = 4.
3. A person facing outward has their right-hand side clockwise: the person immediately to their right is at s - 1 and to their left at s + 1.
4. "Neighbours" and "opposite" do not need direction: neighbours differ by 1 (mod n), opposite by n/2 when n is even.

Worked mini-example: 7 seats, centre-facing, X at 0. Second right = 2, third left = 4; check by counting: going clockwise from 0 gives 6, 5, 4, so the third seat is 4. Same answer.
**Explain simply:**
- Mod n means "wrap round the table".
- Right = anticlockwise comes from standing at the table facing the centre: your right hand points the way the numbers go when viewed from above, anticlockwise.
**Likely follow-ups:** 1) *In a 7-seat circle, who is second to the left of seat 1?* Seat (1 - 2) mod 7 = 6. 2) *What if only some face outward?* Convert each person's right/left on their own with the sign rule.
**Common mistakes / traps:** Using clockwise for "right" when facing the centre; forgetting that the sign flips for outward-facing people; not wrapping past the last seat.

### Q13 ⭐⭐⭐ 🟡 A clue says "A sits between B and C" without the word "immediately". Why can it be read in more than one way, and how do you handle it in a timed test?
**Asked at:** commonly asked (no company-specific report found); wording ambiguity is a known trap in prep-site material (unverified).
**What the interviewer is checking:** Careful reading: "between" and "immediately between" are different clues.
**Say this in the interview:** "Without 'immediately', A just sits somewhere between B and C, with anyone possibly in the gaps. It can also be B then C or C then B. In a test I take the loose reading first, then tighten only when another clue forces adjacency."
**Answer:** **It is ambiguous in two ways: the order (B A C or C A B) and the gaps (adjacent or not). Treat it as 'A is strictly between them in either order, other people allowed in the gaps' unless 'immediately' is written.**
**Step-by-step reasoning:**
1. List both orders: B ... A ... C and C ... A ... B.
2. Do not insist on adjacency unless the word immediately appears.
3. Keep the clue as a constraint ("A's seat is between the seats of B and C") and let the other clues decide.

Worked mini-example: in a row of 5 seats with B, A, C placed in distinct seats there are 60 placements. A is somewhere between B and C in 20 of them. A is immediately between them (all three next to each other) in only 6. Counted by script. So the loose reading allows more than three times as many arrangements.
**Explain simply:**
- "Between" is about order only; "immediately" is about distance.
- A clue that allows many arrangements is weak by itself; it works as a filter later.
**Likely follow-ups:** 1) *Does "A sits between B and C" tell you B is left of C?* No; either order is allowed. 2) *Is "B and C sit on either side of A" the same clue?* It is usually meant as immediate neighbours, but check the puzzle's own wording.
**Common mistakes / traps:** Assuming adjacency (which kills valid arrangements) or assuming a fixed order (B left of C).

### Q14 ⭐⭐⭐ 🟡 What is the difference between "X sits third from the left end" and "X sits third to the left of Y", and how do you avoid mixing them up under time pressure?
**Asked at:** commonly asked (no company-specific report found); position-versus-relative wording is a standard trap in prep-site material (unverified).
**What the interviewer is checking:** Telling an absolute position (counted from an end) from a relative one (counted from another person).
**Say this in the interview:** "Third from the left end is a fixed seat: seat 3. Third to the left of Y depends on where Y is: Y's seat minus 3. The first clue places X directly; the second only links X to Y."
**Answer:** **"Third from the left end" fixes X at seat 3. "Third to the left of Y" means X sits 3 seats left of Y, so X = Y - 3 (and Y is at least seat 4).**
**Step-by-step reasoning:**
1. Number seats 1 to n from the left end.
2. "X third from the left end": X = 3, no other person needed.
3. "X third to the left of Y": X = Y - 3; you need Y first, or you keep it as a relation.
4. In the first case there are 2 people to the left of X; in the second there are 2 people between X and Y.

Worked mini-example: 7 seats. "X third from left end": X = seat 3. "X third to the left of Y" with Y in seat 6: X = 3 too, but with Y in seat 5 it is seat 2. Same words, different place.
**Explain simply:**
- "From the end" counts from a wall; "to the left of" counts from a person.
- Left end and right end are different: third from the right end in 7 seats is seat 5.
**Likely follow-ups:** 1) *In a row of 7, where is "second from the right end"?* Seat 6. 2) *Where is "second to the right of Y" if Y is at seat 4?* Seat 6.
**Common mistakes / traps:** Treating "third to the left of Y" as an end position, or counting yourself as 1 when it is Y's seat plus the step. Under time pressure, underline "from the end" versus "of [person]".

### Q15 ⭐⭐ 🟢 How do you choose between a row diagram, a circle diagram, a grid and a table for different puzzle shapes (row seating, round table, floors, day schedules)?
**Asked at:** commonly asked (no company-specific report found); table-first advice appears on prep sites such as FACE Prep (single-site advice, unverified).
**What the interviewer is checking:** Whether you pick a representation that matches the puzzle's structure.
**Say this in the interview:** "I match the picture to the puzzle: one row of seats gets a row of boxes, a round table gets a circle with seat numbers, floors get a vertical list, days get a timeline, and when there are two attributes, like person and city, I use a table or grid."
**Answer:** **Row for linear seating; circle for round tables; vertical list for floors and stacks; timeline for days or months; grid or table when each person has two or more attributes.**
**Explain simply:**
- Row: direction matters (left/right), so a line with seat numbers 1 to n.
- Circle: no start or end, so fix one person as seat 0 and use mod n.
- Floors and schedules are really the same: numbered slots in a line; "above" or "after" means a higher number.
- Grid or table: use it when people have several features (job, floor, city), and tick yes or no in each cell.

Worked mini-example: "5 people live on floors 1 to 5" is a vertical list (Q1). "7 people at a round table" is a circle with seats 0 to 6 (Q6). "5 sessions across Monday to Friday" is a Mon-Fri timeline (Q10).
**Likely follow-ups:** 1) *How would you draw 6 people, 2 rows of 3, facing each other?* Two parallel rows with compass marks (see Q11). 2) *What if there are 3 attributes?* Use a table with one row per person and one column per attribute.
**Common mistakes / traps:** Reading all clues before drawing anything; or choosing a circle for a row (which loses the "ends" clues).

### Q16 ⭐⭐ 🟡 7 trainees A, B, C, D, E, F and G sit in a row facing north (so each person's right-hand side is towards the east). (1) Exactly 1 person sits between B and F. (2) G sits immediately to the right of C. (3) E sits third to the right of G. (4) A sits immediately to the right of B. Who sits immediately to the left of F?
**Asked at:** commonly asked (no company-specific report found); linear seating is a standard item in prep-site lists for TCS NQT, Accenture and Mu Sigma (prep-site claims, unverified).
**What the interviewer is checking:** Whether you can join clues into blocks ("A right after B" is one unit) and then try the few places each block can go.
**Say this in the interview:** "I join the clues into blocks: B-A, C-G and G...E. The C-G block plus E fills five seats, so only three placements exist. Only one lets B-A and F fit. D sits immediately left of F."
**Answer:** **D** (full row, left to right: C, G, D, F, E, B, A).
**Step-by-step reasoning:**
1. Number the seats 1 to 7 from the left (west) to the right (east). "To the right" means a higher seat number.
2. Clue 4 gives the block B-A (A directly right of B). Clue 2 gives the block C-G. Clue 3 puts E exactly 3 seats right of G, so the pattern is C G _ _ E.
3. That pattern can start at seat 1, 2 or 3 (E must be at seat 7 or lower).
4. Start at seat 1: C1 G2 E5. Free seats are 3, 4, 6, 7. The block B-A needs two touching seats, so it takes 6-7 (B6, A7). Clue 1 (one person between B and F) puts F at seat 4. D takes seat 3. Works.
5. Start at seat 2: C2 G3 E6. Free seats 1, 4, 5, 7. B-A must take 4-5 (B4). F must be at seat 2 or 6, both taken. Fails.
6. Start at seat 3: C3 G4 E7. Free seats 1, 2, 5, 6. B-A takes 1-2 (B1, so F must be at seat 3, taken) or 5-6 (B5, so F must be at seat 3 or 7, both taken). Fails.
7. Final row: seat 1 C, 2 G, 3 D, 4 F, 5 E, 6 B, 7 A. Immediately left of F (seat 4) is seat 3, D.
**Fast method (30 seconds):** Build blocks first, then test the block with the most fixed spacing (here C G _ _ E, only 3 starting seats). Fewer cases than guessing who sits at an end.
**Check:** Brute force over all 5,040 orders: exactly one satisfies all four clues; re-reading each clue against C G D F E B A also passes (B6 and F4 have E between; G2 right of C1; E5 is 3 right of G2; A7 right of B6).
**Explain simply:**
- A "block" is two people glued together by a clue like "immediately right of". Treat it as one unit so there are fewer things to place.
- "Exactly 1 person between" means the two seat numbers differ by 2.
**Likely follow-ups:** 1) *Who sits at the extreme right?* A. 2) *What if clue 4 said A sits immediately to the LEFT of B?* Then the puzzle is no longer unique (brute force finds 2 valid rows: C G A B E F D and D C G A B E F), so the question cannot be answered; this shows why the direction word matters.
**Common mistakes / traps:** Mixing left and right (the row faces north, so right is east, the higher seat number); reading "third to the right" as 2 seats apart instead of 3; stopping at the first fit without checking that the other starts fail.

### Q17 ⭐⭐ 🟡 7 trainees Asha, Bala, Chitra, Dev, Esha, Farid and Gita sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) Dev sits third to the right of Farid. (2) Asha sits immediately to the left of Esha. (3) Dev sits immediately between Asha and Gita. (4) Chitra sits third to the left of Asha. Who sits immediately to the right of Esha?
**Asked at:** commonly asked (no company-specific report found); circular tables facing the centre are a standard format on prep sites for Capgemini, TCS NQT and others (prep-site claims, unverified).
**What the interviewer is checking:** Direction discipline on a circle (right = anticlockwise when facing the centre) and fixing one seat to start.
**Say this in the interview:** "I fix Farid in seat 1 and number seats clockwise. Right means one step anticlockwise. Dev is 3 steps anticlockwise of Farid, Asha and Gita flank Dev, Esha is anticlockwise of Asha, and Chitra is 3 steps clockwise of Asha. Bala is immediately right of Esha."
**Answer:** **Bala**
**Step-by-step reasoning:**
1. Seat the seven places 1 to 7 going clockwise. Convention: facing the centre, your right is the anticlockwise direction, so "right of X" is seat number minus 1 and "left of X" is plus 1 (seat 1 wraps back to seat 7).
2. Put Farid at seat 1 (any seat is fine on a circle, since only relative positions matter). Dev is third to the right: 1 - 3 wraps to seat 5.
3. Dev is between Asha and Gita, so they take seats 4 and 6 in some order.
4. Clue 2: Asha is immediately left of Esha, so Esha is one step anticlockwise of Asha. If Asha is at 6, Esha would be at 5, which Dev holds. So Asha is at 4, Esha at 3, Gita at 6.
5. Clue 4: Chitra is third to the left of Asha: 4 + 3 = seat 7. The last person, Bala, takes seat 2.
6. Clockwise: seat 1 Farid, 2 Bala, 3 Esha, 4 Asha, 5 Dev, 6 Gita, 7 Chitra. Immediately right of Esha (seat 3) is seat 2, Bala.
**Fast method (30 seconds):** Fix the person named in the first clue, then place whoever the clues pin directly (Dev), and use the "between" clue to get two candidates and kill one by a conflict.
**Check:** Brute force over the 720 seatings (one person fixed): exactly one satisfies all clues, and it is the arrangement above. Reading it back: Farid1 to Dev5 is 3 steps anticlockwise; Asha4 is clockwise of Esha3; Dev5 sits between Asha4 and Gita6; Chitra7 is 3 clockwise of Asha4.
**Explain simply:**
- Facing the centre, your right hand points anticlockwise (as seen from above), so "right" moves you down the clockwise numbers.
- Fixing one seat does not lose any arrangement, because rotating a whole circle gives the same seating.
**Likely follow-ups:** 1) *Who sits immediately to the left of Esha?* Asha. 2) *What if everyone faced outside?* Right and left swap (right becomes clockwise), so each "right/left" clue flips.
**Common mistakes / traps:** Treating right as clockwise (it flips every direction clue); forgetting that Asha-Gita can be in either order and eliminating one case by conflict; miscounting "third" as 2 steps.

### Q18 ⭐⭐ 🟡 7 clerks Asha, Bala, Chitra, Dev, Esha, Farid and Gita sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) Bala and Esha are not neighbours. (2) Gita sits immediately between Chitra and Farid. (3) Asha sits second to the left of Gita. (4) Farid sits immediately to the left of Bala. Who sits second to the left of Asha?
**Asked at:** commonly asked (no company-specific report found); circular seating is a standard format on prep sites (unverified).
**What the interviewer is checking:** Using a "between" clue to build a block, then resolving its two orientations with a direction clue and a negative clue.
**Say this in the interview:** "Gita is in the middle of a block Chitra-Gita-Farid. Fix Gita, put Asha two steps left, and let the Farid-Bala clue decide which side Farid is on; the clue that Bala and Esha are not neighbours puts Esha at seat 3. Second left of Asha is Dev."
**Answer:** **Dev**
**Step-by-step reasoning:**
1. Number seats clockwise from Gita at seat 0. Convention: facing the centre, left is clockwise (+1 per step), right is anticlockwise (-1 per step).
2. Asha is second to the left of Gita: seat 2.
3. Gita sits between Chitra and Farid: they take seats 1 and 6 in some order.
4. Clue 4: Farid is immediately left of Bala, so Bala = Farid - 1 (one step anticlockwise). If Farid is at 1, Bala would be seat 0, which is Gita. So Farid is at 6, Bala at 5, Chitra at 1.
5. Seats 3 and 4 remain for Dev and Esha. Clue 1: Bala (5) and Esha are not neighbours; seat 4 touches seat 5, so Esha takes seat 3 and Dev seat 4.
6. Clockwise from Gita: Gita 0, Chitra 1, Asha 2, Esha 3, Dev 4, Bala 5, Farid 6.
7. Second to the left of Asha is 2 + 2 = seat 4, Dev.
**Fast method (30 seconds):** Make the "between" clue a block, fix its middle person, then let the clue naming a direction (Farid left of Bala) rule out one orientation by collision. Use the negative clue last, only to separate the final two seats.
**Check:** Brute force (720 seatings): unique. Without clue 1 the puzzle has 2 solutions (Dev and Esha could swap), so clue 1 is really needed. Reading back: Gita between Chitra and Farid; Asha 2 left of Gita; Farid immediately left of Bala; Bala and Esha are separated by Dev.
**Explain simply:**
- Seat arithmetic wraps around: with 7 seats, seat 6 + 1 is seat 0.
- A negative clue ("not neighbours") is best used at the end to choose between two leftover options.
**Likely follow-ups:** 1) *Who sits immediately right of Bala?* Dev (seat 4). 2) *Drop clue 1: what is the answer?* Not unique: Dev or Esha, so the puzzle fails.
**Common mistakes / traps:** Applying clue 1 first (it only says what is not allowed); placing Farid at seat 1 and forgetting Bala would land on Gita.

### Q19 ⭐⭐ 🟡 7 tenants Asha, Bala, Chitra, Dev, Esha, Farid and Gita live in a 7-floor building, one person per floor, floors numbered 1 (lowest) to 7 (top). (1) Exactly 2 floors lie between the floors of Chitra and Esha. (2) Exactly 3 floors lie between the floors of Bala and Gita. (3) Bala lives on a lower floor than Dev. (4) Dev lives 2 floors above Asha. (5) Exactly 1 floor lies between the floors of Asha and Chitra. (6) Chitra lives on an odd-numbered floor. Who lives immediately above Gita?
**Asked at:** commonly asked (no company-specific report found); floor puzzles are a standard arrangement format on prep sites (unverified).
**What the interviewer is checking:** Turning "exactly k floors between" into "difference of k+1" and testing the few cases a parity clue leaves.
**Say this in the interview:** "Exactly 2 between means floors differ by 3. Chitra is odd, so I try 1, 3, 5, 7. Only Chitra on floor 1 survives. Gita is on 6, so Farid on 7 is immediately above."
**Answer:** **Farid**
**Step-by-step reasoning:**
1. Convert clues to differences: Chitra-Esha differ by 3; Bala-Gita differ by 4; Dev = Asha + 2; Asha-Chitra differ by 2; Bala is below Dev; Chitra is on an odd floor.
2. Since Dev = Asha + 2, Asha is on floor 5 or lower. Asha and Chitra differ by 2, so Asha is odd too.
3. Chitra = 1: Asha 3, Dev 5, Esha 4 (differs by 3 from Chitra). Left: floors 2, 6, 7 for Bala, Gita, Farid. Bala and Gita differ by 4, so they are 2 and 6; Bala is below Dev, so Bala 2, Gita 6, Farid 7. Works.
4. Chitra = 3: Esha must be 6; Asha is 1 (Dev would be 3, taken) or 5 (Dev 7). With Asha 5, Dev 7, the free floors 1, 2, 4 contain no pair differing by 4. Fails.
5. Chitra = 5: Asha 3 gives Dev 5 (taken); Asha 7 gives Dev 9 (does not exist). Fails.
6. Chitra = 7: Asha 5 gives Dev 7 (taken). Fails.
7. Final building: 7 Farid, 6 Gita, 5 Dev, 4 Esha, 3 Asha, 2 Bala, 1 Chitra. Immediately above Gita is Farid.
**Fast method (30 seconds):** Start with the parity clue (4 candidates) and the chain Dev = Asha + 2, which kills many at once. Then use the difference-of-4 clue last, because it needs two free floors far apart.
**Check:** Brute force over all 5,040 assignments: exactly one satisfies all six clues. Re-reading: floors 1 and 4 (Chitra, Esha) have 2 floors between; floors 2 and 6 (Bala, Gita) have 3 between; Asha 3 and Chitra 1 have 1 between.
**Explain simply:**
- "Exactly k floors lie between" means the floor numbers differ by k + 1, because the floors in between are k.
- A parity clue (odd or even) cuts the cases roughly in half.
**Likely follow-ups:** 1) *Without clue 6 is it still unique?* No, brute force finds 2 arrangements, so the parity clue is needed. 2) *Who lives on the top floor?* Farid.
**Common mistakes / traps:** Treating "exactly 2 between" as a difference of 2; forgetting a floor above 7 does not exist (Dev 9); losing track of which of Bala/Gita is higher (clue 3 settles it).

### Q20 ⭐⭐ 🟡 6 boxes coloured Red, Blue, Green, Yellow, Black and White are stacked one on top of another in a single pile. (1) The Blue box is 3 places above the Green box (so 2 boxes lie between them). (2) Exactly 3 boxes lie between the Red and Green boxes. (3) The White box is at the top. (4) The Blue box is 2 places above the Black box (so 1 box lies between them). Which box is fourth from the top?
**Asked at:** commonly asked (no company-specific report found); box and stack puzzles are a variant of floor puzzles on prep sites (unverified).
**What the interviewer is checking:** Mapping a vertical pile to positions 1 to 6 from the top and using the fixed top box to prune cases.
**Say this in the interview:** "White is position 1. Blue is 3 above Green, so Blue is 2 or 3. Blue 2 fails the Red clue, so Blue is 3, Green 6, Black 5, Red 2. The fourth box from the top is Yellow."
**Answer:** **Yellow**
**Step-by-step reasoning:**
1. Number positions 1 (top) to 6 (bottom). White is at 1. "3 places above" means Green's position is Blue's plus 3.
2. Blue cannot be at 1 (White), and Green must be at most 6, so Blue is 2 or 3.
3. Blue = 2: Green 5, Black 4. Red has exactly 3 boxes between itself and Green, so Red would be at position 1 (taken by White) or position 9 (does not exist). Fails.
4. Blue = 3: Green 6, Black 5. Red with 3 between it and Green (6) is position 2. Yellow gets the last place, position 4.
5. Pile, top to bottom: White, Red, Blue, Yellow, Black, Green.
**Fast method (30 seconds):** Use the fixed end (White at the top) to shrink the range for the box with the longest chain (Blue-Green-Black), then test the two cases against the "3 between" clue.
**Check:** Brute force over all 720 orders: unique. Re-read: Blue(3) is 3 above Green(6); between Red(2) and Green(6) are positions 3, 4, 5 (3 boxes); Blue(3) is 2 above Black(5).
**Explain simply:**
- "k boxes between" means positions differ by k + 1; "n places above" means a difference of n.
- Listing positions 1 to 6 in a column is the "diagram": a vertical row.
**Likely follow-ups:** 1) *Which box is second from the bottom?* Black. 2) *Which is directly above Green?* Black.
**Common mistakes / traps:** Reading "3 places above" as "3 between"; not noticing Red could be above or below Green and checking only one side.

### Q21 ⭐⭐ 🟡 6 training modules Excel, SQL, Python, Power BI, Statistics and Tableau are each scheduled on a different day of 6 consecutive days starting Monday, one per day. (1) Tableau is 3 days after SQL. (2) Python is the day after Statistics. (3) Power BI is neither on Monday nor on Saturday. (4) Exactly 1 day separates SQL and Python. (5) Statistics comes earlier in the schedule than Power BI. On which day is Excel?
**Asked at:** commonly asked (no company-specific report found); weekday scheduling puzzles appear in prep-site arrangement sets (unverified).
**What the interviewer is checking:** Placing a block (Statistics then Python) and chaining differences along a timeline.
**Say this in the interview:** "Number Monday to Saturday as 1 to 6. SQL must be on Mon, Tue or Wed because Tableau is 3 days later. Only SQL on Monday survives the Power BI clues. That fills Mon SQL, Tue Statistics, Wed Python, Thu Tableau, Fri Power BI, so Excel is Saturday."
**Answer:** **Saturday**
**Step-by-step reasoning:**
1. Days: Mon, Tue, Wed, Thu, Fri, Sat (1 to 6). Tableau = SQL + 3, so SQL is on Mon, Tue or Wed. SQL and Python have 1 day between them, so Python = SQL + 2 (the other option, SQL - 2, is tried only where it exists). Statistics = Python - 1.
2. SQL = Mon: Python Wed, Statistics Tue, Tableau Thu. Left: Fri, Sat for Excel and Power BI. Power BI is not Saturday, so Power BI Fri, Excel Sat. Statistics (Tue) before Power BI (Fri): yes.
3. SQL = Tue: Tableau Fri, Python Thu, Statistics Wed. Left: Mon, Sat. Power BI is neither Mon nor Sat. Fails.
4. SQL = Wed: Tableau Sat, Python Fri, Statistics Thu. Left: Mon, Tue. Power BI cannot be Mon, so Tue, but Statistics (Thu) must come before Power BI. Fails.
5. Schedule: Mon SQL, Tue Statistics, Wed Python, Thu Tableau, Fri Power BI, Sat Excel.
**Fast method (30 seconds):** The "3 days after" clue limits SQL to three days; the "neither Monday nor Saturday" clue then kills two of them. Test each remaining case quickly.
**Check:** Brute force over all 720 schedules: unique. Without clue 3 (the Power BI day restriction) there are 3 schedules, so that clue matters.
**Explain simply:**
- On a timeline, "n days after" is plus n and "1 day separates" means a gap of 2 days.
- A day-limit clue ("not Monday") is good for finishing cases quickly once the others have narrowed the options.
**Likely follow-ups:** 1) *Which day is Tableau?* Thursday. 2) *Which day is Statistics?* Tuesday.
**Common mistakes / traps:** Reading "exactly 1 day separates" as "next to each other"; checking Power BI's day after fixing others but forgetting Statistics must be before it.

### Q22 ⭐⭐ 🟡 6 new joiners Asha, Bala, Chitra, Dev, Esha and Farid join the company in 6 consecutive months starting January, one per month. (1) Asha joins in February. (2) Exactly 2 months separate Bala and Esha. (3) Exactly 1 month separates Chitra and Esha. (4) Esha joins the month after Farid. (5) Farid joins in May. In which month does Dev join?
**Asked at:** commonly asked (no company-specific report found); month-scheduling items appear in prep-site arrangement sets (unverified).
**What the interviewer is checking:** Starting from the fixed anchors (Farid in May, Asha in February) and working outwards.
**Say this in the interview:** "Farid is May, so Esha is June. Bala is 3 months from Esha: March. Chitra is 2 months from Esha: April. Asha is February, so Dev gets January."
**Answer:** **January**
**Step-by-step reasoning:**
1. Months Jan to Jun are 1 to 6. Farid = 5 (May); Esha is the month after: 6 (June).
2. "Exactly 2 months separate Bala and Esha" means they differ by 3: Bala is 3 (March), since 9 does not exist.
3. "Exactly 1 month separates Chitra and Esha" means they differ by 2: Chitra is 4 (April), since 8 does not exist.
4. Asha = February (given). The only month left is January, so Dev joins in January.
5. Jan Dev, Feb Asha, Mar Bala, Apr Chitra, May Farid, Jun Esha.
**Fast method (30 seconds):** Anchors first, then the "between" clues one at a time, each leaving only one legal month because the other direction runs off the end of the half-year.
**Check:** Brute force over all 720 orders: exactly one fits; re-read: Bala (Mar) and Esha (Jun) have Apr and May between; Chitra (Apr) and Esha (Jun) have May between.
**Explain simply:**
- Months in a 6-month window are positions 1 to 6; there is no wrap past June.
- "Exactly k months separate" means a gap of k + 1.
**Likely follow-ups:** 1) *If Farid joined in April instead?* Then Esha is May, and the same clues fail (brute force finds no valid arrangement), so the original facts matter. 2) *Who joins in April?* Chitra.
**Common mistakes / traps:** Treating "separate by 2" as a gap of 2; forgetting the candidate that runs off the calendar must be discarded.

### Q23 ⭐⭐ 🟡 Eight people sit around a circular table facing the centre (so a person's right-hand side is the anticlockwise direction). Going clockwise from A, the seats are occupied by A, F, C, H, B, E, D and G. Then every person simultaneously moves three seats in the anticlockwise direction (and still faces the centre). Who now sits immediately to the right of A?
**Asked at:** commonly asked (no company-specific report found); "everyone moves" rotation puzzles are a variant of circular seating on prep sites (unverified).
**What the interviewer is checking:** Recognising that a whole-table shift keeps every neighbour relationship unchanged.
**Say this in the interview:** "Everyone moves three seats the same way, so the circle is only rotated. Nobody's neighbours change. A's right neighbour was G before, so it is still G."
**Answer:** **G**
**Step-by-step reasoning:**
1. Original circle clockwise: A, F, C, H, B, E, D, G (and back to A).
2. Facing the centre, "right" is the anticlockwise direction. Going anticlockwise from A, the next person is G (the last name in the list).
3. Moving every person 3 seats anticlockwise is a rotation of the whole circle. The order around the table does not change, so everyone keeps the same neighbours.
4. After the move the circle reads (clockwise) H, B, E, D, G, A, F, C. Immediately anticlockwise of A is G again.
**Fast method (30 seconds):** If all people move the same number of seats in the same direction, answer from the original order. Do not redraw the circle.
**Check:** Computed by script: new seat positions give A with G immediately anticlockwise; the original and shifted orders differ only by rotation.
**Explain simply:**
- Rotating a circle changes seat numbers, not who is next to whom.
- Right and left (facing the centre) depend only on the circular order, so they survive a rotation.
**Likely follow-ups:** 1) *What if all move 2 seats clockwise instead?* Still G. 2) *What if only A moved 3 seats?* Then the neighbours change and you must redraw.
**Common mistakes / traps:** Thinking the "right" neighbour is the one now sitting in A's old right-hand seat (that person moved too).

### Q24 ⭐⭐ 🟡 A company pays salaries on the last working day (Monday to Friday, ignoring public holidays) of every month. On which dates are the January, February and March 2026 salaries paid? (1 January 2026 is a Thursday.)
**Asked at:** commonly asked (no company-specific report found); calendar puzzles are a variant of the date and day questions in aptitude sets (unverified).
**What the interviewer is checking:** Working out weekdays from one known date, then stepping back from a weekend to the previous Friday.
**Say this in the interview:** "1 January is Thursday, so 31 January is a Saturday; pay moves back to Friday 30 January. February has 28 days in 2026 and ends on Saturday, so 27 February. March ends on Tuesday 31 March."
**Answer:** **Fri 30 January 2026, Fri 27 February 2026, Tue 31 March 2026.**
**Step-by-step reasoning:**
1. A week has 7 days, so days in a month beyond 28 shift the weekday by (days - 28) mod 7.
2. Jan 1 is Thursday. Jan 31 is 30 days later; 30 mod 7 = 2, so Thursday + 2 = Saturday. Last working day is Friday 30 January.
3. Jan 31 is Saturday, so Feb 1 is Sunday. 2026 is not a leap year (February has 28 days), so Feb 28 is Saturday. Last working day is Friday 27 February.
4. Mar 1 is Sunday; March has 31 days, so Mar 31 = Sunday + 30 days = Sunday + 2 = Tuesday. A working day, so salary on 31 March.
**Fast method (30 seconds):** Compute the last day's weekday by (last date - 1) mod 7 from the first day's weekday. If it is Saturday, subtract 1; if Sunday, subtract 2.
**Check:** Verified with Python's calendar module: 30 Jan (Fri), 27 Feb (Fri), 31 Mar (Tue).
**Explain simply:**
- Working day here means Monday to Friday; public holidays are ignored as the question says.
- 28 days always repeat the same weekday pattern, so only the extra days matter.
**Likely follow-ups:** 1) *April and May 2026?* Thursday 30 April and Friday 29 May (31 May is a Sunday); checked by script. 2) *What if 2026 were a leap year?* February would end on Sunday 29 and the pay date would be Friday 27 February again.
**Common mistakes / traps:** Paying on the calendar-last date even when it is a weekend; forgetting 2026 is not a leap year.

### Q25 ⭐⭐ 🟡 A team holds its review on the 2nd and 4th Tuesday of every month. In a 31-day month that starts on a Sunday, on which dates are the reviews held?
**Asked at:** commonly asked (no company-specific report found); calendar puzzles are a variant of aptitude day questions (unverified).
**What the interviewer is checking:** Mapping the day of the week to dates and counting the nth occurrence.
**Say this in the interview:** "If the 1st is a Sunday, Tuesday is the 3rd. Tuesdays are the 3rd, 10th, 17th, 24th and 31st. The 2nd and 4th are the 10th and 24th."
**Answer:** **The 10th and the 24th.**
**Step-by-step reasoning:**
1. The 1st is Sunday, so the 2nd is Monday and the 3rd is Tuesday.
2. Tuesdays then fall every 7 days: 3, 10, 17, 24, 31 (31 is within the 31-day month).
3. The 2nd Tuesday is the 10th; the 4th Tuesday is the 24th.
**Fast method (30 seconds):** First occurrence of the weekday = 1 + (days from the 1st to that weekday); then add 7 for the 2nd, 21 for the 4th.
**Check:** Verified by script (Tuesdays 3, 10, 17, 24, 31). Note the 5th Tuesday (31st) is not a review day.
**Explain simply:**
- "2nd Tuesday" counts only Tuesdays, not the 2nd date of the month.
- Weekday cycles repeat every 7 days.
**Likely follow-ups:** 1) *Month starts on a Wednesday?* Tuesdays are 7, 14, 21, 28, so reviews on 14th and 28th (checked by script). 2) *Which dates if the 1st is a Tuesday?* 8th and 22nd.
**Common mistakes / traps:** Counting Tuesday as 2 (assuming Sunday is day 0); treating the 2nd Tuesday as the 2nd date.

### Q26 ⭐⭐ 🟡 A help desk is covered by Rahul on every 3rd day and by Sana on every 4th day, counting both from 1 March 2026 (so both are on duty on 1 March). On which dates in March 2026 are both on duty on the same day.
**Asked at:** commonly asked (no company-specific report found); repeating-cycle (LCM) rosters appear in prep-site sets (unverified).
**What the interviewer is checking:** Seeing it as a least-common-multiple (LCM) problem on a repeating cycle.
**Say this in the interview:** "Both start on 1 March; Rahul repeats every 3 days and Sana every 4, so they coincide every 12 days: 1, 13 and 25 March."
**Answer:** **1, 13 and 25 March 2026.**
**Step-by-step reasoning:**
1. Rahul is on duty on days 1, 4, 7, 10, 13, ... (every 3rd day starting day 1).
2. Sana is on duty on days 1, 5, 9, 13, ... (every 4th day starting day 1).
3. Both repeat together after the LCM of 3 and 4, which is 12. From day 1: day 1, day 13, day 25 (day 37 is past 31 March).
4. These are Sunday 1 March, Friday 13 March and Wednesday 25 March.
**Fast method (30 seconds):** Both start on day 1, so add the LCM (12) to 1 repeatedly until you pass the month end.
**Check:** Verified by script (days where (d-1) is divisible by both 3 and 4: 1, 13, 25).
**Explain simply:**
- LCM (least common multiple) is the smallest number both cycle lengths divide into evenly; two cycles line up again after exactly that many days.
- The common start (both on 1 March) means the pattern begins together.
**Likely follow-ups:** 1) *If Sana were every 6th day?* LCM is 6: 1, 7, 13, 19, 25, 31 March (checked). 2) *Which weekday is 13 March 2026?* Friday (1 March is a Sunday, plus 12 days).
**Common mistakes / traps:** Starting the count from 0 and answering 3, 15, 27; stopping at the first overlap; using 3 x 4 only by luck (fails when numbers share a factor).

### Q27 ⭐⭐ 🟡 In how many ways can 6 distinct people sit around a circular table if two particular people, A and B, must sit next to each other? (Two seatings that differ only by rotating everyone are the same; a seating and its mirror image are counted as different.)
**Asked at:** commonly asked (no company-specific report found); permutation counting for seating is a standard aptitude topic on prep sites (unverified).
**What the interviewer is checking:** Gluing a pair into one unit, using the circular rule (n - 1)!, and remembering the pair's internal order.
**Say this in the interview:** "Glue A and B as one unit. That makes 5 units around the table: (5 - 1)! = 24 circular arrangements. A and B can swap inside the block: times 2. Total 48."
**Answer:** **48**
**Step-by-step reasoning:**
1. Treat A and B as one block: now 5 objects (the block and the 4 other people).
2. Circular arrangements of 5 distinct objects, with rotations counted as the same, is (5 - 1)! = 24.
3. Inside the block, A-B or B-A: 2 ways.
4. Total = 24 x 2 = 48.
**Fast method (30 seconds):** Together: glue, then (units - 1)! x 2. Apart: total minus together (see Q28).
**Check:** Brute force over all arrangements with one person fixed: 48 seatings where A and B are neighbours.
**Explain simply:**
- Rotations of the same circle are the same seating, so fix one seat and arrange the rest: (n - 1)!.
- "Next to each other" can happen in two orders, so multiply by 2.
**Likely follow-ups:** 1) *7 people instead of 6?* (6 - 1)! x 2 = 240 (brute force confirms). 2) *If mirror images counted as the same?* 48 / 2 = 24 (confirmed by script, since no arrangement here equals its own mirror).
**Common mistakes / traps:** Using 4! x 2 (forgetting the block counts as one object) or 5! (treating it like a row).

### Q28 ⭐⭐ 🟡 In how many ways can 7 distinct people sit around a circular table if two particular people, A and B, must not sit next to each other? (Rotations are the same seating; mirror images are different.)
**Asked at:** commonly asked (no company-specific report found); "not together" counting is a standard topic on prep sites (unverified).
**What the interviewer is checking:** The complement method: total minus the "together" case.
**Say this in the interview:** "Total circular seatings of 7 people is 6! = 720. Seatings with A and B together: glue them to get 6 units, 5! x 2 = 240. Not together: 720 - 240 = 480."
**Answer:** **480**
**Step-by-step reasoning:**
1. Total for 7 people around a circle (rotations the same): (7 - 1)! = 720.
2. A and B together: glue them, 6 units, (6 - 1)! = 120, times 2 internal orders = 240.
3. Not together = 720 - 240 = 480.
**Fast method (30 seconds):** "Not" counts are easiest as total minus together.
**Check:** Brute force over all 720 arrangements with one person fixed: 480 have A and B not adjacent.
**Explain simply:**
- Complement counting means count everything, then subtract the cases you do not want.
- It avoids listing the many different ways A and B can be apart.
**Likely follow-ups:** 1) *6 people?* 5! - 2 x 4! = 120 - 48 = 72 (checked by script). 2) *Probability they are together?* 240 / 720 = 1/3.
**Common mistakes / traps:** Forgetting the factor 2 for the glued pair; using 7! as the total.

### Q29 ⭐⭐ 🟡 In how many ways can 4 analysts and 4 managers, all distinct, sit around a circular table so that analysts and managers alternate? (Rotations are the same seating; mirror images are different.)
**Asked at:** commonly asked (no company-specific report found); alternating-group counting is a standard topic on prep sites (unverified).
**What the interviewer is checking:** Fixing one person to break the rotation, then arranging each group in its own seats.
**Say this in the interview:** "Fix one analyst. The other 3 analysts take the remaining 3 analyst seats: 3! ways. The 4 managers fill the 4 gaps: 4! ways. 6 x 24 = 144."
**Answer:** **144**
**Step-by-step reasoning:**
1. Alternating means seats go analyst, manager, analyst, manager around the table, 8 seats.
2. Fix one analyst in any seat (this removes the rotation duplicates). The analyst seats are now decided: every second seat.
3. The other 3 analysts fill the 3 remaining analyst seats: 3! = 6.
4. The 4 managers fill the 4 manager seats: 4! = 24.
5. Total = 6 x 24 = 144.
**Fast method (30 seconds):** (analysts - 1)! x managers!. Fix one from the group you pick to anchor.
**Check:** Brute force over all arrangements with one person fixed: 144 alternating seatings.
**Explain simply:**
- Rotations are the same, so anchoring one analyst is allowed (every valid seating has an analyst we can rotate to that seat).
- Once the pattern analyst, manager, ... is set, the two groups are independent of each other.
**Likely follow-ups:** 1) *5 analysts and 5 managers?* 4! x 5! = 2880 (brute force confirms). 2) *Mirror images the same?* The count would be 144 / 2 = 72.
**Common mistakes / traps:** Using 4! x 4! = 576 (forgetting to fix one for rotation) or 8!/something.

### Q30 ⭐⭐ 🟡 In how many ways can 5 distinct people sit in a row of 5 chairs if two particular people, A and B, must not sit next to each other?
**Asked at:** commonly asked (no company-specific report found); "not together" counting in a row is a standard topic on prep sites (unverified).
**What the interviewer is checking:** The complement method in a row (where rotation does not apply).
**Say this in the interview:** "A row of 5 has 5! = 120 orders. With A and B glued: 4 units, 4! x 2 = 48. Not together: 120 - 48 = 72."
**Answer:** **72**
**Step-by-step reasoning:**
1. Total orders of 5 people in a row: 5! = 120 (no rotation shortcut in a row).
2. A and B together: glue them, 4 units, 4! = 24, times 2 internal orders = 48.
3. Not together = 120 - 48 = 72.
**Fast method (30 seconds):** Row, not together: n! - 2 x (n - 1)!. Here 120 - 48.
**Check:** Brute force over all 120 orders: 72 have A and B not adjacent.
**Explain simply:**
- A row has two ends; a circle does not, so the formulas differ.
- Complement counting avoids listing the ways A and B can be apart.
**Likely follow-ups:** 1) *6 chairs?* 720 - 240 = 480 (confirmed). 2) *Probability that A and B are together in the row of 5?* 48 / 120 = 2/5.
**Common mistakes / traps:** Using the circular formula (n - 1)! for a row; forgetting the factor 2.

### Q31 ⭐⭐ 🟡 How do you handle a clue that creates two possible cases (for example "A sits at one of the two ends"), and when is it better to branch into cases than to look for another clue?
**Asked at:** commonly asked (no company-specific report found); seating and arrangement puzzles are listed as a standard section on prep-site pages (unverified).
**What the interviewer is checking:** Whether you can keep two possibilities alive in an organised way instead of guessing one.
**Say this in the interview:** "I draw one small diagram per case, push each case forward with the other clues, and cross out the case that breaks a clue. Branching is worth it when no clue fixes a person directly."
**Answer:** **Write each case as its own mini-diagram, test it against the remaining clues, and drop any case that contradicts one. Branch only when no direct clue (a fixed seat, a "between" or "immediately" clue) is left to use first.**
**Step-by-step reasoning:**
1. Look for a clue that fixes someone for certain. Use those first; they cost nothing.
2. If none is left and a clue says "one of two places", name the cases: Case 1 and Case 2.
3. Build both diagrams side by side and apply every remaining clue to each.
4. A case that breaks any clue is dead. If one case survives, you are done; if both survive, the puzzle is ambiguous or the asked answer is the same in both.
Mini-example (checked by script): 5 people in a row, A at one end, B and A exactly two seats apart, C immediately right of B, D somewhere left of A. Case 1 (A at the left end): D cannot be to the left of A, so this case dies. Case 2 (A at the right end): B is third from the left, so D E B C A or E D B C A; the only survivors.
**Check:** Brute force over all 120 orders of the mini-example gave exactly those 2 arrangements, both with A at the right end.
**Explain simply:**
- A "case" is one possible reading of an either/or clue. Cases are cheap when each one dies fast.
- Branching is a last resort: using fixed clues first usually shrinks the choices so that one case is killed at once.
**Likely follow-ups:** 1) *What if both cases survive?* Check whether the question's answer is the same in both; if it is, answer it, if not, re-read the clues for a missed word such as "immediately". 2) *How many cases is too many?* More than about three suggests you skipped a firmer clue.
**Common mistakes / traps:** Picking one case "because it looks natural" and never testing the other, or mixing the two cases in one diagram.

### Q32 ⭐⭐ 🟡 Why can you fix one person's seat at a circular table without losing any arrangement, and in which situations is that shortcut not allowed?
**Asked at:** commonly asked (no company-specific report found); circular-table puzzles are a listed standard format on prep sites (unverified).
**What the interviewer is checking:** Whether you understand why a circle has no fixed "first seat", and can state the limits of that trick.
**Say this in the interview:** "A circle can be turned without changing who sits next to whom, so I pin one person to any seat as an anchor and arrange the rest relative to them. I would not do it if the seats themselves are distinguishable, such as numbered seats or one facing a door."
**Answer:** **Rotating everyone gives the same seating, so one person's seat can be fixed freely; it is not allowed when the seats are labelled or a landmark makes them different.**
**Step-by-step reasoning:**
1. With 5 labelled seats there are 5! = 120 ways to place 5 people.
2. Each real seating (who is next to whom) appears 5 times, once for each rotation, so 120 / 5 = 24 distinct seatings.
3. Fixing one person at one seat leaves the other 4 to arrange: 4! = 24. Same answer, so nothing is lost.
4. After you fix one person, you may not fix a second: the others are now measured from the anchor.
Not allowed when: seats are numbered or named (labelled seats, so rotations are different); a clue points to a fixed place (the door, the north side, "opposite the window"); or you are counting arrangements where seat identity matters, in which case the count is n!.
**Check:** Verified by script for n = 3 to 7: the number of distinct seatings (rotations merged) was 2, 6, 24, 120, 720, equal to (n - 1)!.
**Explain simply:**
- "Rotation" means everyone moves the same number of seats; neighbours do not change.
- Fixing a person is just choosing where to start measuring.
**Likely follow-ups:** 1) *In the Q42 style puzzle, who do you fix?* The person named most often in the clues. 2) *With 6 numbered seats and 6 people?* 6! = 720, no division.
**Common mistakes / traps:** Fixing two people, or fixing someone at a "special" seat when that seat is not actually special.

### Q33 ⭐⭐ 🟡 How many distinct seatings of n different people around a circular table are there, and what changes in the count if the table can be turned over so that mirror images count as the same?
**Asked at:** commonly asked (no company-specific report found); circular arrangement counting is a typical aptitude topic (unverified).
**What the interviewer is checking:** The (n - 1)! rule and the mirror-image adjustment, with the edge cases.
**Say this in the interview:** "Fix one person to remove rotations, then the rest can be arranged in (n - 1)! ways. If a seating and its mirror image count as the same, halve it: (n - 1)! / 2, valid for n of 3 or more."
**Answer:** **(n - 1)! distinct seatings; (n - 1)! / 2 if mirror images are counted as the same (for n at least 3).**
**Step-by-step reasoning:**
1. n! orders around n labelled seats; each seating appears n times by rotation, so n! / n = (n - 1)!.
2. Turning the table over reverses the clockwise order. For n at least 3 the reversed seating is a different list, so they pair up and the count halves.
3. Table (checked by script):

| n | (n - 1)! | (n - 1)! / 2 |
|---|---|---|
| 3 | 2 | 1 |
| 4 | 6 | 3 |
| 5 | 24 | 12 |
| 6 | 120 | 60 |
| 7 | 720 | 360 |

**Check:** Verified by script: for n = 3 to 7 the brute-force counts matched the table, for both rules.
**Explain simply:**
- "Distinct" means nobody has a different neighbour pair arrangement; rotating all does not count as new.
- Halving applies when the object has no front and back, such as a necklace or a table you can flip. People who face the centre have a left and a right, so mirror images are normally different and you do not halve.
**Likely follow-ups:** 1) *n = 2?* 1 seating; the halving formula would give 0.5, so it only works for n of 3 or more. 2) *8 people, mirror images different?* 7! = 5040.
**Common mistakes / traps:** Using n! for a circle, or halving in a seating puzzle where the question says mirror images differ.

### Q34 ⭐⭐ 🟡 In a floor or stack puzzle, which diagram do you draw, and how do you use clues such as "exactly k floors between" efficiently?
**Asked at:** commonly asked (no company-specific report found); floor and stack puzzles are a listed standard format on prep sites (unverified).
**What the interviewer is checking:** Choosing a vertical number line and translating "between" counts into position gaps.
**Say this in the interview:** "I draw a vertical column of numbered boxes. 'Exactly k floors between' means the two floor numbers differ by k + 1."
**Answer:** **Draw a vertical list of floors (1 at the bottom); "exactly k floors between" means a floor-number gap of k + 1, and for a fixed k there are only (number of floors) - (k + 1) possible position pairs.**
**Step-by-step reasoning:**
1. Draw floors from the top number down to 1, one box each.
2. Place fixed clues first: "top floor", "floor 1", "lives on floor 4".
3. Convert "exactly k floors between X and Y" into |X - Y| = k + 1, so for 7 floors and k = 2 the gap is 3 and the pairs are (1,4), (2,5), (3,6), (4,7).
4. Convert "k floors above" into plain addition: X = Y + k.
5. Chain the clues (D = A + 2, B = A + 5) into one column.
Counts of possible pairs for 7 floors (checked by script): k = 1 gives 5, k = 2 gives 4, k = 3 gives 3, k = 5 gives 1. Bigger gaps leave fewer options, so start with the largest gap.
**Check:** Verified by script: unordered pairs with gap k + 1 in 7 floors are 6 - k.
**Explain simply:**
- "Between" counts only the floors strictly between, not the two people, so add 1.
- "Above" and "higher" mean a bigger number; "immediately above" means exactly +1.
**Likely follow-ups:** 1) *Gap of 3 floors between, 6 floors?* Floor gap 4: pairs (1,5) and (2,6), 2 pairs. 2) *Same stack, 'between' without 'exactly'?* Then only gap at least 2 is known.
**Common mistakes / traps:** Using the count of floors between as the floor difference (off by one), and drawing the stack upside down.

### Q35 ⭐⭐ 🟡 How do you handle day and month schedules that wrap around (Sunday to Monday, December to January), and which clue wordings make the wrap-around matter?
**Asked at:** commonly asked (no company-specific report found); weekday and month schedule puzzles are a common prep-site format (unverified).
**What the interviewer is checking:** Comfort with cyclic counting (clock arithmetic) in weeks and years.
**Say this in the interview:** "I number the days 0 to 6 or the months 1 to 12 and use remainders, so after Sunday comes Monday and after December comes January."
**Answer:** **Treat the days or months as a circle: move forward or back with remainder arithmetic (mod 7 for days, mod 12 for months); wrap-around matters whenever a clue says "after", "before" or "k days later" across the week or year end, or says the roster repeats.**
**Step-by-step reasoning:**
1. Number Monday = 0 to Sunday = 6 (or January = 0 to December = 11).
2. "k days after X" is (X + k) mod 7; "k days before" is (X - k) mod 7.
3. Examples (checked by script): Saturday + 3 days = Tuesday; Monday - 2 days = Saturday; November + 3 months = February; January - 2 months = November.
4. If the question says "one per day of a 7-day week, Monday to Sunday" and no "repeats" wording, ask whether wrap-around is allowed; a plain "Monday to Sunday" list may not wrap.
Wording that makes wrap-around matter: "the day after Sunday", "two days before Monday", "the roster repeats every week", "next month" at December.
**Check:** Verified by script: the four examples above were computed with remainders.
**Explain simply:**
- "Mod 7" means divide by 7 and keep the remainder, like a clock with 7 hours.
- A circle has no end, so a clue can step past the last label and arrive at the first.
**Likely follow-ups:** 1) *What day is 100 days after Monday?* 100 mod 7 = 2, so Wednesday (hand-checked). 2) *If the schedule does not repeat?* Then no wrap: the clue must fit inside Monday to Sunday.
**Common mistakes / traps:** Stopping at Sunday and calling a clue impossible, or applying wrap-around to a schedule that is a single week.

### Q36 ⭐⭐ 🟡 How do you verify a finished arrangement against all clues in about 30 seconds, and why is this check worth the time in an online assessment?
**Asked at:** commonly asked (no company-specific report found); verification habits are standard prep-site advice, not a company-specific finding.
**What the interviewer is checking:** Discipline: do you test your answer instead of trusting a hunch?
**Say this in the interview:** "I re-read each clue once against my finished diagram, ticking it off. It takes about half a minute and catches the common slips."
**Answer:** **Go through the clues one at a time in the original order, test each against the final arrangement, and look especially for direction and "immediately / between" wording; it is worth it because one mistake in the base arrangement ruins every question in the set.**
**Step-by-step reasoning:**
1. Write the final arrangement in a single line or circle with seat numbers.
2. Read clue 1 aloud in your head, find the people, and tick or cross.
3. Repeat for every clue; do not skip the negative ones ("not next to").
4. Check that every person appears once and the count of seats is right.
5. Re-read the question itself: "right of", "second to the left", "opposite" must match what you computed.
**Fast method (30 seconds):** Check direction words first (left/right, above/below, before/after) because they are the most common slip, then the number words (second, third, exactly k between).
**Check:** This is itself the check; for the puzzles in this book every final arrangement was also confirmed by brute force.
**Explain simply:**
- A "set" shares one arrangement across 4 to 5 questions, so an early error repeats.
- Checking costs seconds; a wrong base costs the whole set.
**Likely follow-ups:** 1) *What if a clue fails?* Find the earliest deduction that used it and redo from there. 2) *Is it worth it on the last 2 minutes?* Our suggestion: check the base arrangement, not each answer.
**Common mistakes / traps:** Re-reading from memory instead of from the printed clues, and checking only the positive clues.

### Q37 ⭐⭐ 🟡 A puzzle set has one arrangement and five questions. How do you decide whether to invest the time in building the full arrangement, and what do you do if you are stuck after two minutes?
**Asked at:** commonly asked (no company-specific report found); one prep-site guide (FACE Prep) suggests about 3 to 4 minutes per arrangement set (single third-party claim, unverified).
**What the interviewer is checking:** Time judgement under a clock, not just puzzle skill.
**Say this in the interview:** "A shared arrangement is worth building when five questions ride on it. If I am stuck after two minutes I stop, mark the set, take the questions that need fewer clues, and come back."
**Answer:** **Build the full arrangement when it earns several questions and at least a few clues are direct; if you are stuck after two minutes, branch on one either/or clue or move on and return. These are our suggestions, not research findings.**
**Step-by-step reasoning:**
1. Skim the clues for firm ones (a fixed seat, "extreme end", "immediately next to").
2. Our rule of thumb: if you can place at least two people in about 30 seconds, invest.
3. Five questions on one arrangement, even if each is worth one mark, are five marks for one diagram, a better rate than five separate puzzles.
4. If after two minutes you have not found a firm placement, try one case-branch for about a minute (see Q31).
5. Still stuck: answer the questions that may not need the full arrangement, guess if there is no negative marking (check the test's rules), and move on.
**Check:** Hand-checked: this is judgement, not computed; adjust the timings to your own practice results.
**Explain simply:**
- "Shared arrangement" means one puzzle with several questions about it.
- Time spent is lost for other questions, so a stuck puzzle is a trap.
**Likely follow-ups:** 1) *What if there is negative marking?* Do not guess blindly; guess only when you can remove at least one option. 2) *Easy sets first?* Yes, our suggestion: collect quick marks first.
**Common mistakes / traps:** Sinking 6 minutes into one set out of pride, or skipping a set just because it looks long even though it has strong early clues.

### Q38 ⭐⭐ 🟡 Why is it usually better to apply negative clues such as "A does not sit next to B" after you have a partial arrangement instead of using them to place people first?
**Asked at:** commonly asked (no company-specific report found); "apply negative clues last" is standard prep-site advice (unverified).
**What the interviewer is checking:** Whether you know which clues cut the possibilities most.
**Say this in the interview:** "A negative clue only rules out a few arrangements, so it does little to place anyone. I use the positive clues to build a partial arrangement and then let the negative ones choose between the leftover options."
**Answer:** **Positive clues (immediately right, third from the left) shrink the possibilities a lot; negative clues ("not next to") remove few, so they are best used as a final filter on a partial arrangement.**
**Step-by-step reasoning:**
1. Take 5 people in a row: 120 arrangements in total.
2. "A and B are not next to each other" leaves 72 of them (60%).
3. "B sits immediately right of A" leaves only 24 (20%).
4. So the positive clue does more of the placing; the negative one leaves far too many ways to choose from.
5. After the partial arrangement is built, a negative clue usually decides between two remaining spots in one step.
**Check:** Verified by script over all 120 orders: 72 satisfy the negative clue, 24 the positive one.
**Explain simply:**
- A "negative clue" says what is not true. It points nowhere, it only crosses out.
- A "positive clue" says where someone is, so you can draw them.
**Likely follow-ups:** 1) *Can a negative clue ever place someone?* Yes, when only two spots are left and one is excluded. 2) *When do you use it early?* If it is the only clue about that person.
**Common mistakes / traps:** Spending time trying to place people using "not next to" first, or forgetting to apply it at all and answering with an arrangement that breaks it.

### Q39 ⭐⭐ 🔴 8 analysts Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit in a row facing north (so each person's right-hand side is towards the east). (1) Gita sits somewhere to the left of Bala. (2) Farid and Hari do not sit next to each other. (3) Asha sits immediately to the right of Esha. (4) Bala sits immediately between Dev and Gita. (5) Esha sits second from the left end. (6) Exactly 3 persons sit between Dev and Hari. Who sits second to the left of Bala?
**Asked at:** commonly asked (no company-specific report found); 8-person rows are a harder variant of a standard prep-site format (unverified).
**What the interviewer is checking:** Combining fixed-position clues with a "between" block and a gap count.
**Say this in the interview:** "Esha is second from the left and Asha is right after her. Bala sits between Gita and Dev with Gita on the left, so the block is Gita, Bala, Dev. Dev and Hari have 3 people between, which fixes the block's spot. Second to the left of Bala is Chitra."
**Answer:** **Chitra.**
**Step-by-step reasoning:**
1. Seats 1 to 8, left to right. Esha = 2 (clue 5), Asha = 3 (clue 3).
2. Clues 1 and 4: Gita is left of Bala and Bala is between Dev and Gita, so the block is Gita, Bala, Dev in three consecutive seats.
3. The block cannot use seats 2 or 3, so it starts at seat 4 or later: seats 4-6, 5-7 or 6-8. (Seat 1 is a single seat before Esha, too small.)
4. Clue 6: Hari is 4 seats from Dev (3 between). If Dev is at 6 or 7, Hari would be at 2 or 3 (taken) or 10 or 11, which does not exist. So Dev is at 8 and Hari is at 4.
5. Block: Gita 6, Bala 7, Dev 8. Remaining people Chitra and Farid take seats 1 and 5. Clue 2 (Farid and Hari not next to each other): Hari is at 4, so Farid cannot be at 5; Farid = 1, Chitra = 5.
Final row: 1 Farid, 2 Esha, 3 Asha, 4 Hari, 5 Chitra, 6 Gita, 7 Bala, 8 Dev. Second to the left of Bala (seat 7) is seat 5: Chitra.
**Fast method (30 seconds):** Place the fixed pair (Esha, Asha), merge the "between" clues into one 3-seat block, then use the gap clue to test where the block fits.
**Check:** Verified by script over all 8! = 40,320 orders: exactly one satisfies all six clues.
**Explain simply:**
- A "block" is people who must stay together, treated as one item.
- "Exactly 3 between" means seat numbers differ by 4.
**Likely follow-ups:** 1) *Who is third from the right end?* Gita (seat 6). 2) *If clue 2 were dropped?* Farid and Chitra could swap, so the arrangement and the answer would not be unique; checked by reasoning.
**Common mistakes / traps:** Putting Dev left of Bala (reading "between" without using clue 1), or reading "exactly 3 between" as a seat gap of 3.

### Q40 ⭐⭐ 🔴 8 candidates A, B, C, D, E, F, G and H sit in a row facing north (so each person's right-hand side is towards the east). (1) G sits third to the right of F. (2) C sits immediately to the right of H. (3) Exactly 2 persons sit between A and C. (4) B sits somewhere to the left of A. (5) C sits second to the right of E. (6) G sits immediately to the right of B. Who sits immediately to the right of F?
**Asked at:** commonly asked (no company-specific report found); 8-person rows are a harder variant of a standard prep-site format (unverified).
**What the interviewer is checking:** Chaining many relative-position clues into one row and testing where the chains fit.
**Say this in the interview:** "Clues 1 and 6 make one chain: F, one seat, B, G. Clues 2 and 5 make E, H, C side by side. I slide those chains along the 8 seats and apply the A clues. Only F D B G A E H C works, so immediately right of F is D."
**Answer:** **D.**
**Step-by-step reasoning:**
1. Clue 6: B then G (adjacent). Clue 1: G is 3 seats right of F. So F is at seat f, B at f + 2, G at f + 3, with one unknown seat (call it x) at f + 1.
2. Clues 2 and 5: H is immediately left of C, and E is 2 seats left of C, so E, H, C are three seats side by side.
3. Clue 4: B is left of A. Clue 3: A and C have exactly 2 between (3 seats apart).
4. Try each f. f = 1: x is seat 2, and A or D goes there; A must be right of B, so x = D; seats 5 to 8 hold A and E H C: A E H C has C at 8 and A at 5 (gap 3, correct); E H C A has A next to C (wrong).
5. f = 2: E H C must take 6 to 8, A would sit left of B (wrong). f = 3: no 3 free seats in a row. f = 4: E H C takes 1 to 3, A is then at seat 8, 5 seats from C (wrong). f = 5: A cannot be right of B (wrong).
Final row: F D B G A E H C.
**Fast method (30 seconds):** Write each clue as a chain, then slide the 4-seat chain along the row; most positions die within a few seconds.
**Check:** Verified by script over all 8! = 40,320 orders: exactly one arrangement, F D B G A E H C.
**Explain simply:**
- "Third to the right of F" means 3 seats along, so 2 people are between them.
- A chain is a group whose relative positions are fixed; you then only choose where the whole chain starts.
**Likely follow-ups:** 1) *Who is third from the left end?* B. 2) *Who sits between A and C?* E and H.
**Common mistakes / traps:** Reading "second to the right of E" as one seat away (it is two seats), which puts C one seat too early.

### Q41 ⭐⭐ 🔴 8 HR executives Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit in a row facing north (so each person's right-hand side is towards the east). (1) Farid sits third to the right of Esha. (2) Esha sits immediately between Chitra and Hari. (3) Dev sits somewhere to the left of Gita. (4) Exactly 2 persons sit between Bala and Hari. (5) Asha sits second to the right of Gita. Who sits second to the right of Hari?
**Asked at:** commonly asked (no company-specific report found); 8-person rows are a harder variant of a standard prep-site format (unverified).
**What the interviewer is checking:** Handling a "between" clue whose order is not given, by testing both orders.
**Say this in the interview:** "Esha is between Chitra and Hari but I do not know which side each is on, so I test both orders at each possible seat of Esha. Only Chitra, Esha, Hari at seats 3, 4, 5 survives, giving Dev, Bala, Chitra, Esha, Hari, Gita, Farid, Asha. Second right of Hari is Farid."
**Answer:** **Farid.**
**Step-by-step reasoning:**
1. Seats 1 to 8, left to right. Clue 1: Farid = Esha + 3, so Esha is in seats 1 to 5; clue 2 needs a neighbour on each side, so Esha is in seats 2 to 5.
2. Clue 4: Bala and Hari have exactly 2 between, so their seats differ by 3. Clue 5: Asha is 2 seats right of Gita. Clue 3: Dev is left of Gita.
3. For each order of the trio (Chitra, Esha, Hari or Hari, Esha, Chitra) and each Esha seat from 2 to 5, place Bala 3 seats from Hari, then see whether the three remaining people fit Gita, Asha (2 right of Gita) and Dev (left of Gita).
4. Seven of the eight combinations fail, for example Hari, Esha, Chitra with Esha at seat 2 forces Gita 6, Asha 8, Dev 7, which breaks "Dev left of Gita".
5. The survivor: Chitra 3, Esha 4, Hari 5, Farid 7, Bala 2, then Gita 6, Asha 8, Dev 1.
Row: 1 Dev, 2 Bala, 3 Chitra, 4 Esha, 5 Hari, 6 Gita, 7 Farid, 8 Asha.
**Fast method (30 seconds):** Use the rigid chain first (Esha and Farid 3 apart), then the 3-seat gap clue, and leave the order of the trio to the end.
**Check:** Verified by script over all 40,320 orders: exactly one arrangement, and the 8 order-and-seat combinations were enumerated separately: only one has a solution.
**Explain simply:**
- "Esha between Chitra and Hari" means the three sit together with Esha in the middle, in either order.
- Testing both orders is quicker than guessing.
**Likely follow-ups:** 1) *Who sits at the extreme right?* Asha. 2) *Who is immediately left of Esha?* Chitra.
**Common mistakes / traps:** Assuming Chitra is on the left because she is named first, and reading "exactly 2 between" as a seat gap of 2 instead of 3.

### Q42 ⭐⭐ 🔴 8 managers Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) Asha sits third to the right of Gita. (2) Bala sits second to the left of Hari. (3) Dev sits second to the left of Farid. (4) Esha sits second to the left of Bala. (5) Bala and Farid are neighbours. Who sits second to the right of Gita?
**Asked at:** commonly asked (no company-specific report found); 8-person circles are a harder variant of a standard prep-site format (unverified).
**What the interviewer is checking:** Turning "right/left by k" into seat arithmetic on a circle with the facing-centre convention.
**Say this in the interview:** "Facing the centre, my right is anticlockwise. I fix Gita at seat 0 and number clockwise, so k to the right is minus k. Everything chains off Bala, and only one placement works. Second to Gita's right is Chitra."
**Answer:** **Chitra.**
**Step-by-step reasoning:**
1. Seats 0 to 7 clockwise; Gita = 0. Right of X by k means seat of X minus k; left means plus k.
2. Clue 1: Asha = 0 - 3 = seat 5.
3. Let Bala = b. Clue 2: Hari = b - 2. Clue 4: Esha = b + 2. Clue 5: Farid = b + 1 or b - 1. Clue 3: Dev = Farid + 2.
4. If Farid = b - 1 (Dev = b + 1): the free seats are b + 3, b + 4, b + 5, and Gita and Asha must be 5 seats apart (Asha = Gita + 5); none of the pairs fits. Dead.
5. If Farid = b + 1 (Dev = b + 3): free seats are b - 1, b + 4, b + 5. Gita = b - 1 and Asha = b + 4 fits, so Chitra = b + 5. With Gita = 0, b = 1.
Final, clockwise from Gita: 0 Gita, 1 Bala, 2 Farid, 3 Esha, 4 Dev, 5 Asha, 6 Chitra, 7 Hari. Second to Gita's right is seat 6: Chitra.
**Fast method (30 seconds):** Anchor the person who appears in the first clue, write everyone as "b + something" around one chain, and let the leftover seats test the anchor clue.
**Check:** Verified by script (Gita fixed, 7! = 5,040 seatings): exactly one arrangement; all five clues re-read against the final circle.
**Explain simply:**
- "Second to the right" means two seats along on that person's right-hand side.
- Fixing one person is allowed because rotating everyone gives the same seating (see Q32).
**Likely follow-ups:** 1) *Who sits opposite Gita?* Dev (seat 4). 2) *Who is second to Gita's left?* Farid (seat 2).
**Common mistakes / traps:** Treating clockwise as "right"; that mirrors the whole table and gives a different, wrong answer.

### Q43 ⭐⭐ 🔴 8 analysts Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) Esha sits third to the right of Hari. (2) Bala sits third to the right of Dev. (3) Chitra and Hari are not neighbours. (4) Esha and Gita are not neighbours. (5) Bala sits immediately between Farid and Hari. (6) Farid sits third to the left of Chitra. Who sits third to the left of Gita?
**Asked at:** commonly asked (no company-specific report found); 8-person circles are a harder variant of a standard prep-site format (unverified).
**What the interviewer is checking:** Using the rigid clues first and the negative ("not neighbours") clues last.
**Say this in the interview:** "I fix Hari at seat 0. Bala is next to Hari with Farid on the far side of Bala, so there are two cases. One case breaks the Chitra clue, the other works, and the negative clues place Gita and Asha. Third to Gita's left is Asha."
**Answer:** **Asha.**
**Step-by-step reasoning:**
1. Seats 0 to 7 clockwise; Hari = 0. Right of X by k is seat minus k; left is plus k.
2. Clue 1: Esha = 0 - 3 = seat 5. Clue 5: Bala is at seat 1 or 7, and Farid is on the other side of Bala (seat 2 or 6).
3. Clue 2: Dev = Bala + 3. Clue 6: Chitra = Farid - 3.
4. Bala = 1: Farid = 2, Dev = 4, Chitra = 7, next to Hari, which clue 3 forbids. Dead.
5. Bala = 7: Farid = 6, Dev = 2, Chitra = 3. Asha and Gita take seats 1 and 4. Seat 4 is next to Esha (5), and clue 4 says Gita is not Esha's neighbour, so Gita = 1 and Asha = 4.
Final, clockwise from Hari: 0 Hari, 1 Gita, 2 Dev, 3 Chitra, 4 Asha, 5 Esha, 6 Farid, 7 Bala. Third to Gita's left is seat 1 + 3 = 4: Asha.
**Fast method (30 seconds):** Take the rigid chain (Farid, Bala, Hari) first; the negative clues then choose between the last two seats.
**Check:** Verified by script (Hari fixed, 7! = 5,040 seatings): exactly one arrangement; all six clues re-read against it.
**Explain simply:**
- "Not neighbours" is a negative clue: it only crosses options out, so use it last (see Q38).
- "Neighbours" means the seat on either side, in both directions.
**Likely follow-ups:** 1) *Who sits opposite Bala?* Chitra (seat 3). 2) *Who is immediately right of Hari?* Bala (seat 7).
**Common mistakes / traps:** Counting "third to the left" in the wrong direction, and dropping the "Bala = 1" case without checking it against the Chitra clue.

### Q44 ⭐⭐ 🔴 8 candidates Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) Hari sits third to the right of Bala. (2) Farid sits second to the right of Gita. (3) Gita sits immediately between Esha and Hari. (4) Chitra sits opposite Esha. (5) Chitra sits second to the right of Dev. Who sits opposite Farid?
**Asked at:** commonly asked (no company-specific report found); 8-person circles with an "opposite" clue are a harder variant of a standard prep-site format (unverified).
**What the interviewer is checking:** Using "opposite" (4 seats away on an 8-seat circle) together with relative clues.
**Say this in the interview:** "On 8 seats, opposite means 4 seats apart. Gita sits between Esha and Hari, so I try both sides. One side puts Dev on Hari's seat, so it dies. The other fills the circle, and opposite Farid is Asha."
**Answer:** **Asha.**
**Step-by-step reasoning:**
1. Seats 0 to 7 clockwise; Gita = 0. Right of X by k is seat minus k.
2. Clue 3: Esha and Hari are seats 1 and 7 in some order. Clue 2: Farid = 0 - 2 = seat 6.
3. Esha = 1, Hari = 7: Chitra is opposite Esha, seat 5, and clue 5 puts Dev at 5 + 2 = seat 7, already Hari. Dead.
4. Esha = 7, Hari = 1: Chitra = seat 3, Dev = 5. Clue 1: Bala = Hari + 3 = seat 4. Asha takes seat 2.
Final, clockwise from Gita: 0 Gita, 1 Hari, 2 Asha, 3 Chitra, 4 Bala, 5 Dev, 6 Farid, 7 Esha. Opposite Farid (6) is seat 2: Asha.
**Fast method (30 seconds):** On an 8-seat circle, "opposite" always adds 4. Place the trio first, then test each side.
**Check:** Verified by script (7! = 5,040 seatings): exactly one arrangement; all five clues re-read against it.
**Explain simply:**
- Opposite = half-way round = n / 2 seats away (here 4); this works only when n is even.
- Each "k to the right" becomes "minus k seats" on a clockwise-numbered circle.
**Likely follow-ups:** 1) *Who sits opposite Bala?* Gita. 2) *With 7 people?* Nobody is exactly opposite.
**Common mistakes / traps:** Using 3 or 5 seats for "opposite", or swapping left and right.

### Q45 ⭐⭐ 🔴 7 colleagues Asha, Bala, Chitra, Dev, Esha, Farid and Gita sit around a circular table. Asha, Bala, Dev and Gita face the centre and Chitra, Esha and Farid face outside (away from the centre). 'Right' and 'left' are from each person's own point of view, so for a person facing the centre the right-hand side is the anticlockwise direction, and for a person facing outside it is the clockwise direction. (1) Dev sits immediately to the left of Bala. (2) Gita sits third to the left of Asha. (3) Bala sits second to the left of Farid. (4) Chitra sits third to the left of Dev. Who sits immediately to the right of Chitra?
**Asked at:** commonly asked (no company-specific report found); circular practice sets with some people facing outside are described on GeeksforGeeks (prep site, unverified).
**What the interviewer is checking:** Switching the left/right rule for each person when facings differ.
**Say this in the interview:** "I read each clue from the viewpoint of the person it counts from. Facing the centre, left is clockwise; facing out, left is anticlockwise. That makes Bala, Dev, Farid three seats in a row, and the rest falls out. Immediately right of Chitra is Esha."
**Answer:** **Esha.**
**Step-by-step reasoning:**
1. Fix Asha = seat 0, numbered clockwise. Centre-facers: left = clockwise (plus), right = minus. Outward-facers: left = minus, right = plus.
2. Clue 2: Gita = 0 + 3 = seat 3.
3. Clue 1: Dev = Bala + 1 (Bala faces the centre). Clue 3: Bala = Farid - 2 (Farid faces out, so his left is anticlockwise), so Farid = Bala + 2. Bala, Dev, Farid are three seats in a row.
4. Seats 0 (Asha) and 3 (Gita) are taken, so the only run of 3 free seats is 4, 5, 6: Bala 4, Dev 5, Farid 6.
5. Clue 4: Chitra = Dev + 3 = seat 1 (Dev faces the centre). Esha takes the last seat, 2.
Final, clockwise from Asha: 0 Asha, 1 Chitra (out), 2 Esha (out), 3 Gita, 4 Bala, 5 Dev, 6 Farid (out). Chitra faces out, so her right is clockwise: seat 2, Esha.
**Fast method (30 seconds):** Mark each person C (centre) or O (out) first, then convert every "left/right k" using that person's own flag.
**Check:** Verified by script (Asha fixed, 6! = 720 seatings): exactly one arrangement when each clue is read from the viewpoint of the person it counts from (the person after "of"). Reading clues 2 to 4 the other way still gave Esha, but reading clue 1 the other way gave no valid seating.
**Explain simply:**
- Facing the opposite way swaps which direction round the table is left and which is right.
- Always ask "whose left?" before counting; the question states it is each person's own view.
**Likely follow-ups:** 1) *Who sits immediately to the left of Chitra?* Asha (Chitra faces out, so left is anticlockwise: seat 0). 2) *Who sits second to the right of Chitra?* Gita (Chitra faces out, so right is clockwise: seat 1 + 2 = 3). Hand-checked.
**Common mistakes / traps:** Using the centre-facing rule for everyone, which breaks the seating or gives a wrong answer.

### Q46 ⭐⭐ 🔴 8 analysts Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit around a circular table. Chitra, Esha, Farid and Gita face the centre and Asha, Bala, Dev and Hari face outside (away from the centre). 'Right' and 'left' are from each person's own point of view, so for a person facing the centre the right-hand side is the anticlockwise direction, and for a person facing outside it is the clockwise direction. (1) Hari sits immediately between Chitra and Gita. (2) Farid sits immediately between Asha and Bala. (3) Esha sits immediately to the right of Asha. (4) Chitra sits third to the right of Asha. Who sits second to the right of Asha?
**Asked at:** commonly asked (no company-specific report found); circular tables with people facing the centre or outside are described as a standard format on prep sites (unverified).
**What the interviewer is checking:** Whether you handle "right" correctly for people who face outward, and build the circle from the tightest clues first.
**Say this in the interview:** "For someone facing outside, right is clockwise, so I fix Asha, place Esha and Chitra from her, then use the two 'between' clues. Dev sits second to the right of Asha."
**Answer:** **Dev**
**Step-by-step reasoning:**
1. Number the seats 1 to 8 clockwise (as seen from above). Rule: facing the centre, right = anticlockwise (seat number goes down); facing outside, right = clockwise (seat number goes up).
2. Put Asha (outside) in seat 1. Clue 3: Esha is immediately to her right = seat 2. Clue 4: Chitra is third to her right = seat 4.
3. Clue 2: Farid is between Asha and Bala. Asha's neighbours are seats 2 and 8; seat 2 is Esha, so Farid = seat 8 and Bala = seat 7.
4. Clue 1: Hari is between Chitra and Gita, so Hari is seat 3 or 5. If Hari were seat 3, Gita would have to be seat 2, which is Esha. So Hari = seat 5, Gita = seat 6.
5. Dev takes the last seat, 3.
Final circle, clockwise from seat 1: Asha (out), Esha (in), Dev (out), Chitra (in), Hari (out), Gita (in), Bala (out), Farid (in).
Second to the right of Asha (outside, so clockwise 2 steps) = seat 3 = Dev.
**Fast method (30 seconds):** Start from the person who appears in the most clues (Asha) and convert every "right/left" into a plus or minus on seat numbers before touching the other clues.
**Check:** Brute force over all arrangements (Asha fixed in seat 1, 5,040 ways): exactly one satisfies all four clues, and it gives Dev (verified by script).
**Explain simply:**
- Right and left belong to the person speaking about it, so reverse the direction for each person who faces outside.
- "Between" clues put a person next to two named people, so they pin the circle quickly.
**Likely follow-ups:** *Who sits immediately to the right of Chitra?* Chitra faces the centre, so right = anticlockwise = seat 3 = Dev (verified by script).
**Common mistakes / traps:** Using the centre-facing rule for Asha (that would put Esha in seat 8 and build the wrong circle); forgetting that Esha, a centre-facer, still sits on the clockwise side of Asha.

### Q47 ⭐⭐ 🔴 Four analysts (Asha, Bala, Dev and Farid) and four managers (Chitra, Esha, Gita and Hari) sit around a circular table facing the centre (so a person's right-hand side is the anticlockwise direction), alternating so that no two analysts and no two managers sit next to each other. (1) Asha does not sit opposite Dev. (2) Bala sits third to the right of Gita. (3) Bala sits third to the left of Hari. (4) Farid sits second to the right of Asha. (5) Dev and Esha are neighbours. Who sits second to the right of Gita?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Using a hidden structure (alternating groups means odd and even seats) to cut the search, and using the "does not sit opposite" clue as a filter.
**Say this in the interview:** "Alternating means analysts take every other seat. Clues 2 and 3 fix Bala, Gita and Hari relative to each other, clues 4 and 1 place the analysts, and the answer is Chitra."
**Answer:** **Chitra**
**Step-by-step reasoning:**
1. Seats 1 to 8 clockwise, everyone faces the centre, so right = anticlockwise (seat number goes down), left = clockwise (up).
2. Clue 2: Bala = Gita minus 3. Clue 3: Bala = Hari plus 3. So Gita = Bala + 3 and Hari = Bala minus 3 (same as Bala + 5). Put Bala in seat 5: Gita = seat 8, Hari = seat 2.
3. Analysts take alternate seats, so the analysts are in seats 1, 3, 5, 7: Bala is 5, so Asha, Dev, Farid fill 1, 3, 7. Managers are in 2, 4, 6, 8.
4. Clue 4: Farid = Asha minus 2. Options: Asha 1 and Farid 7, or Asha 3 and Farid 1.
5. If Asha is 3, Dev is 7, directly opposite Asha, which clue 1 forbids. So Asha = 1, Farid = 7, Dev = 3.
6. Clue 5: Esha is next to Dev (seat 3), so seat 2 or 4. Seat 2 is Hari, so Esha = 4 and Chitra = 6.
Circle clockwise: Asha, Hari, Dev, Esha, Bala, Chitra, Farid, Gita.
Second to the right of Gita (seat 8) = seat 6 = Chitra.
**Fast method (30 seconds):** Combine two clues about the same person (Bala) into one relation, fix that person anywhere (rotation does not matter on a circle), then use parity (odd or even seat) for the alternating groups.
**Check:** Brute force over all 5,040 circles (Asha fixed) with the alternating rule: one solution, Chitra (verified by script).
**Explain simply:**
- "Alternating" means seat parity tells you the group, so half the seats are ruled out for each person.
- On a circle only the relative order matters, so you may fix one person anywhere.
**Likely follow-ups:** *Without clue 1, is it still unique?* No. A second circle fits the other clues: Asha, Chitra, Bala, Esha, Dev, Gita, Farid, Hari (clockwise). There Asha is opposite Dev and the answer would be Esha, so clue 1 is what makes the answer unique (verified by script).
**Common mistakes / traps:** Forgetting that opposite seats on 8 seats are 4 apart; treating "does not sit opposite" as a mere decoration when it is the clue that kills a case.

### Q48 ⭐⭐ 🔴 7 employees Asha, Bala, Chitra, Dev, Esha, Farid and Gita live in a 7-floor building, one person per floor, floors numbered 1 (lowest) to 7 (top). (1) Farid lives on the floor immediately between those of Bala and Gita. (2) Asha lives immediately above Bala. (3) Gita lives on an even-numbered floor. (4) Esha lives on neither the top floor nor floor 1. (5) Exactly 2 floors lie between the floors of Dev and Farid. How many floors lie between the floors of Chitra and Farid?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Building a block of consecutive floors from "immediately" clues, then testing the few cases left.
**Say this in the interview:** "Farid is in the middle of Bala and Gita, and Asha sits on Bala, so Gita, Farid, Bala, Asha form a block of four floors. Testing the even floor for Gita leaves one layout, and there are 3 floors between Chitra and Farid."
**Answer:** **3 floors**
**Step-by-step reasoning:**
1. Let Farid live on floor f. Bala and Gita are on floors f-1 and f+1 in some order. Asha is immediately above Bala.
2. If Bala were on f-1, Asha would be on f, which is Farid's floor. So Gita = f-1, Bala = f+1, Asha = f+2: a block of four.
3. Gita's floor f-1 is even and the block must fit under floor 7, so Gita is on floor 2 or 4.
4. Gita on 2: Farid 3, Bala 4, Asha 5. Dev is 3 floors from Farid (2 floors between), so Dev = 6. Chitra and Esha are left with floors 1 and 7, but Esha cannot be on 1 or 7. Fails.
5. Gita on 4: Farid 5, Bala 6, Asha 7. Dev = floor 2. Left: floors 1 and 3. Esha is not on 1, so Esha = 3, Chitra = 1.
Floors 7 to 1: Asha, Bala, Farid, Gita, Esha, Dev, Chitra.
Chitra is on 1, Farid on 5: floors 2, 3, 4 lie between = 3.
**Fast method (30 seconds):** Merge "immediately above/between" clues into one block, then slide the block using the parity or end-floor clues.
**Check:** Brute force over all 5,040 assignments: exactly one satisfies all five clues (verified by script).
**Explain simply:**
- "Exactly 2 floors lie between" means the floor numbers differ by 3, not 2.
- Clues that give a floor's property (even, not top) are checks on a case, not placements.
**Likely follow-ups:** *Who lives immediately above Esha?* Gita (floor 4 over floor 3).
**Common mistakes / traps:** Reading "exactly 2 between" as a difference of 2; forgetting that Bala could be on the lower side of Farid and checking that Asha's floor then clashes.

### Q49 ⭐⭐ 🔴 8 flat-owners Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari live in an 8-floor building, one person per floor, floors numbered 1 (lowest) to 8 (top). (1) Esha lives 3 floors above Dev. (2) Chitra lives on a lower floor than Asha. (3) Gita lives 2 floors above Esha. (4) Exactly 3 floors lie between the floors of Chitra and Farid. (5) Exactly 1 floor lies between the floors of Asha and Esha. (6) Exactly 1 floor lies between the floors of Farid and Hari. Who lives immediately below Dev?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Turning "k floors above" and "exactly k between" clues into number differences and eliminating cases.
**Say this in the interview:** "Dev, Esha and Gita are linked by fixed gaps, so only three starting floors are possible. I test each; only Dev on floor 3 works, and Bala is directly below him."
**Answer:** **Bala**
**Step-by-step reasoning:**
1. Let Dev be on floor d. Esha = d+3, Gita = d+5, so d is 1, 2 or 3 (Gita must be on floor 8 or lower).
2. Asha is one floor between her and Esha, so Asha = Esha +/- 2. Chitra is below Asha. Farid is 4 floors from Chitra (3 between). Hari is 2 from Farid.
3. d = 1: Esha 4, Gita 6, Asha 2 (6 is taken). Chitra must be below 2, so floor 1, but Dev is there. Fails.
4. d = 2: Esha 5, Gita 7, Asha 3 (7 is taken). Chitra is 1 (2 is Dev). Farid = 5, but Esha is there. Fails.
5. d = 3: Esha 6, Gita 8, Asha 4. Chitra below 4: floor 1 or 2. Farid = Chitra + 4 = 5 or 6; 6 is Esha, so Chitra = 1, Farid = 5. Hari = 7 (3 is Dev). Bala = 2.
Floors 1 to 8: Chitra, Bala, Dev, Asha, Farid, Esha, Hari, Gita.
Directly below Dev (floor 3) is floor 2 = Bala.
**Fast method (30 seconds):** Write all floors as d + something; the allowed range of d usually leaves 2 or 3 cases.
**Check:** Brute force over all 40,320 assignments: exactly one satisfies all six clues (verified by script).
**Explain simply:**
- Chains of "k above" clues tie several people to one unknown, so you solve for that one unknown.
- "Exactly 3 floors lie between" means a difference of 4.
**Likely follow-ups:** *Who lives on the floor directly above Farid?* Esha.
**Common mistakes / traps:** Using a difference of 3 for "3 between"; forgetting that Asha could be above or below Esha.

### Q50 ⭐⭐ 🔴 7 boxes coloured Red, Blue, Green, Yellow, Black, White and Orange are stacked one on top of another in a single pile. (1) The Black box is somewhere below the Red box. (2) The Blue box is somewhere below the Black box. (3) The Red and Orange boxes are not touching. (4) The Orange box is 3 places above the Yellow box (so 2 boxes lie between them). (5) The White box is 2 places above the Red box (so 1 box lies between them). Which box is directly above the White box?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Treating a stack as a vertical row and combining ordering clues with exact gaps.
**Say this in the interview:** "I number positions from the bottom. Blue under Black under Red forces Red to position 3 or more, White is two above Red, and testing Red at 3, 4 and 5 leaves only Red at 3. Green is directly above White."
**Answer:** **Green**
**Step-by-step reasoning:**
1. Positions 1 (bottom) to 7 (top). Blue < Black < Red in position, so Red is at least 3. White = Red + 2 must be 7 or less, so Red is 3, 4 or 5.
2. Red 5: White 7. Orange = Yellow + 3: the options (Yellow 1, Orange 4) and (Yellow 3, Orange 6) both put Orange next to Red, which clue 3 forbids. Fails.
3. Red 4: White 6. Blue and Black fill two of positions 1, 2, 3. Orange = Yellow + 3 only works as Yellow 2, Orange 5, which touches Red. Fails.
4. Red 3: Blue 1, Black 2, White 5. Left for Yellow and Orange: 4, 6, 7. Orange = Yellow + 3 gives Yellow 4, Orange 7. Green takes 6.
Stack from bottom: Blue, Black, Red, Yellow, White, Green, Orange.
The box directly above White (position 5) is position 6 = Green.
**Fast method (30 seconds):** Anchor on the chain with the most ordering (Blue, Black, Red) to limit Red, then test each value.
**Check:** Brute force over all 5,040 stacks: one satisfies every clue (verified by script).
**Explain simply:**
- "Somewhere below" only orders two boxes; "3 places above" fixes an exact gap.
- "Not touching" is only a way to reject a case.
**Likely follow-ups:** *Which box is at the bottom?* Blue.
**Common mistakes / traps:** Counting from the top by accident; reading "3 places above" as 3 boxes in between.

### Q51 ⭐⭐ 🔴 7 HR reviews payroll audit, attendance review, hiring report, exit survey, training audit, budget review and policy refresh are each scheduled on a different day of 7 consecutive days starting Monday, one per day. (1) Exit survey and budget review are not on consecutive days. (2) Exactly 1 day separates hiring report and policy refresh. (3) Exactly 3 days separate attendance review and hiring report. (4) Attendance review is on Wednesday. (5) Hiring report is 3 days after payroll audit. (6) Exactly 3 days separate exit survey and policy refresh. Which review is scheduled on Tuesday?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Converting "exactly k days separate" to day differences and chaining fixed days.
**Say this in the interview:** "Attendance is Wednesday, so hiring is Sunday, which puts payroll on Thursday and policy on Friday. Exit survey is then Monday, budget cannot be Tuesday, so Tuesday is training audit."
**Answer:** **Training audit**
**Step-by-step reasoning:**
1. Convention: "exactly 3 days separate" means 3 days lie in between (the days differ by 4); "3 days after" means a difference of 3.
2. Attendance is Wednesday. Hiring is 3 days between, so Sunday (Wednesday minus 4 would be before Monday).
3. Payroll is 3 days before hiring: Thursday.
4. Policy is 1 day between with hiring: Friday.
5. Exit is 3 days between with policy (Friday): Monday (the other side would be after Sunday).
6. Left: Tuesday and Saturday for training audit and budget review. Clue 1: exit (Monday) and budget are not consecutive, so budget is not Tuesday. Budget = Saturday, training audit = Tuesday.
Week: Mon exit survey, Tue training audit, Wed attendance review, Thu payroll audit, Fri policy refresh, Sat budget review, Sun hiring report.
**Fast method (30 seconds):** Begin with the clue that names an actual day, and chain outward.
**Check:** Brute force over all 5,040 schedules: exactly one fits (verified by script).
**Explain simply:**
- Number days Monday = 1 to Sunday = 7 and use differences.
- "Separate" counts the days between, "after" counts the step.
**Likely follow-ups:** *Which review is on Saturday?* The budget review (step 6).
**Common mistakes / traps:** Reading "3 days separate" as a difference of 3, which shifts every later day.

### Q52 ⭐⭐ 🔴 7 client calls Asha, Bala, Chitra, Dev, Esha, Farid and Gita are each scheduled on a different day of 7 consecutive days starting Monday, one per day. (1) Farid is 3 days after Dev. (2) Asha comes earlier in the schedule than Gita. (3) Bala is 2 days after Asha. (4) Chitra is 3 days after Farid. On which day is Esha?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Chaining equal steps and noticing that a chain can only fit in one place in a week.
**Say this in the interview:** "Dev, Farid and Chitra are three steps apart, so they span Monday to Sunday exactly. That leaves four days and I place Asha, Bala and Gita. Esha is Tuesday."
**Answer:** **Tuesday**
**Step-by-step reasoning:**
1. Chitra = Farid + 3 = Dev + 6. With 7 days (0 to 6) Dev must be Monday, Farid Thursday, Chitra Sunday.
2. Free days: Tuesday, Wednesday, Friday, Saturday for Asha, Bala, Gita, Esha.
3. Bala = Asha + 2. Asha on Tuesday puts Bala on Thursday (taken). Asha on Friday puts Bala on Sunday (taken). Asha on Wednesday puts Bala on Friday. Asha cannot be on Saturday.
4. Asha is on Wednesday, Bala on Friday. Gita must be later than Asha: Saturday (Tuesday is earlier).
5. Esha takes Tuesday.
Week: Dev, Esha, Asha, Farid, Bala, Gita, Chitra.
**Fast method (30 seconds):** A chain of exact steps that nearly fills the week fixes its own start.
**Check:** Brute force over all 5,040 schedules: one satisfies all four clues (verified by script).
**Explain simply:**
- "Three days after" means position plus 3.
- "Earlier" only orders, it does not give a gap.
**Likely follow-ups:** *Which day is Gita?* Saturday.
**Common mistakes / traps:** Trying to place Asha first when the Dev-Farid-Chitra chain is the tight one.

### Q53 ⭐⭐ 🔴 8 people A, B, C, D, E, F, G and H sit in two parallel rows of 4. Row 1 faces south and row 2 faces north, so each person in one row sits directly opposite (faces) exactly one person in the other row. 'Right' and 'left' are from each person's own point of view. (1) E does not sit at either end of a row. (2) A and H sit in the same row. (3) B and H sit in different rows. (4) D sits in row 1. (5) A does not sit at either end of a row. (6) F faces H. (7) C sits immediately to the right of D. (8) D sits at one end of a row. (9) B faces E. Who faces D?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you reverse left and right for the row that faces the other way, and keep columns aligned.
**Say this in the interview:** "I draw two rows with columns west to east. Row 1 faces south, so its right is west. D must be at the east end of row 1 for C to sit on its right. That fixes everything and G faces D."
**Answer:** **G**
**Step-by-step reasoning:**
1. Draw columns 1 to 4 from west to east. Row 1 faces south, so its right-hand side is west. Row 2 faces north, so its right-hand side is east.
2. D is in row 1 at an end, and C is immediately to D's right. D in column 1 would have no seat to its west, so D is in column 4 and C in column 3 (row 1).
3. B faces E, so they are in different rows. A and H are in the same row. If A and H were in row 1, they would take columns 1 and 2, and then B and E (needing different rows) would be in row 2 together, which is impossible. So A and H are in row 2.
4. B is in a different row from H, so B is in row 1. E is then in row 2. F faces H, so F is in row 1. Row 1 has C, D, B, F; row 2 has A, H, E, G.
5. Row 1 has C, D in columns 3, 4, so B and F fill columns 1 and 2. In row 2, E and A are not at the ends, so they take columns 2 and 3 and H, G take the ends. F is in column 1 or 2 and faces H, who is at an end, so F is column 1 and H column 1. Then B is column 2 and faces E (column 2), A is column 3 and G column 4.
Row 1 (faces south, west to east): F, B, C, D
Row 2 (faces north, west to east): H, E, A, G
The person facing D (column 4) is G.
**Fast method (30 seconds):** Place the clue with an end and a left/right relation first; it fixes the column and the row.
**Check:** Brute force over all 40,320 placements: one arrangement satisfies all nine clues (verified by script).
**Explain simply:**
- Two people face each other only if they are in the same column of different rows.
- Row 1 looks south, so its left and right are the opposite of row 2.
**Likely follow-ups:** *Who sits immediately to the left of D?* Row 1 left is east; nobody is east of D. D is at the east end, so D has no one immediately to its left.
**Common mistakes / traps:** Using the same right direction for both rows; putting B and E in the same row.

### Q54 ⭐⭐ 🔴 8 people A, B, C, D, E, F, G and H sit in two parallel rows of 4. Row 1 faces south and row 2 faces north, so each person in one row sits directly opposite (faces) exactly one person in the other row. 'Right' and 'left' are from each person's own point of view. (1) A sits immediately to the right of G. (2) B and G sit in different rows. (3) D sits immediately to the left of H. (4) C faces G. (5) B faces D. (6) F sits immediately to the right of B. (7) D sits in row 2. Who faces H?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Reversing left/right for each row and using "faces" clues to move between rows.
**Say this in the interview:** "I first decide rows: B faces D so B is in row 1, then G, C, A, H share the rows. Row 2 must read G A D H from west to east, which leaves E facing H."
**Answer:** **E**
**Step-by-step reasoning:**
1. Columns 1 to 4 run west to east. Row 1 faces south (right = west). Row 2 faces north (right = east).
2. D is in row 2 and B faces D, so B is in row 1. B and G are in different rows, so G is in row 2; C faces G, so C is in row 1.
3. A sits next to G (same row), so A is in row 2. H is next to D, so H is in row 2. Row 2 holds G, A, D, H; row 1 holds B, C, F, E.
4. A is immediately right of G: G, A are consecutive from west to east. H is immediately right of D: D, H consecutive. So row 2 is G A D H or D H G A.
5. F is immediately right of B in row 1, which means F is west of B. In D H G A, D is in column 1, so B is in column 1 and F has no seat to its west. Fails. So row 2 is G A D H.
6. B faces D (column 3), so B is column 3; F is column 2; C faces G (column 1); E is column 4.
Row 1 (south, west to east): C, F, B, E
Row 2 (north, west to east): G, A, D, H
H is in column 4, so E faces H.
**Fast method (30 seconds):** Settle which person is in which row first (just using "faces" and "different row" clues), then fix columns.
**Check:** Brute force over all 40,320 placements: one arrangement satisfies all seven clues (verified by script).
**Explain simply:**
- "Faces" means same column, other row.
- A reversed row flips every "right" and "left" clue.
**Likely follow-ups:** *If clue 3 were read the other way (H immediately left of D), would the answer change?* Yes: that wrong reading gives two arrangements and the answer becomes F (checked by script), which shows how a misread left/right can hide the unique answer.
**Common mistakes / traps:** Treating "D immediately to the left of H" as "H is to the left of D".

### Q55 ⭐⭐ 🔴 Seven analysts Asha, Bala, Chitra, Dev, Esha, Farid and Gita each take night duty on a different day of the week, one per day, Monday to Sunday. The roster repeats every week, so Sunday is followed by Monday. (1) Dev is on duty on Monday. (2) Esha is on duty the day before Dev. (3) Chitra is on duty the day before Esha. (4) Gita is on duty the day before Bala. (5) Asha is on duty the day after Bala. (6) Farid is on duty two days after Bala. Who is on duty on Friday?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Working modulo 7 (the week wraps around) and using a block of consecutive days.
**Say this in the interview:** "Dev, Esha and Chitra fill Monday, Sunday and Saturday. Gita, Bala, Asha, Farid are four consecutive days and must sit in Tuesday to Friday, so Gita is Tuesday and Farid is Friday."
**Answer:** **Farid**
**Step-by-step reasoning:**
1. Dev is Monday. Esha is the day before: Sunday (the week wraps). Chitra is the day before Esha: Saturday.
2. Clues 4 to 6 say Gita, Bala, Asha, Farid are on four consecutive days in that order (Gita, then Bala next day, Asha the day after, Farid the day after that).
3. The days left are Tuesday, Wednesday, Thursday, Friday, which are exactly four consecutive days, so Gita is Tuesday, Bala Wednesday, Asha Thursday, Farid Friday.
Roster: Mon Dev, Tue Gita, Wed Bala, Thu Asha, Fri Farid, Sat Chitra, Sun Esha.
Friday is Farid.
**Fast method (30 seconds):** Write the chains as blocks, then drop each block into the gap the fixed days leave.
**Check:** Brute force over all 5,040 rosters with Sunday followed by Monday: one fits (verified by script).
**Explain simply:**
- "Wrap around" means the day after Sunday is Monday, like clock arithmetic.
- A block of four consecutive days can sit only in a gap of four days.
**Likely follow-ups:** *Who is on duty on Sunday?* Esha.
**Common mistakes / traps:** Putting Esha on a day before Monday that does not exist and giving up; not noticing the block fits only one gap.

### Q56 ⭐⭐ 🔴 Eight people live in a 4-floor building with two flats (west and east) on each floor, one person per flat, floors numbered 1 (lowest) to 4 (top). (1) Gita and Hari live on the same side of the building with exactly one floor between them. (2) Esha and Gita live on the same floor. (3) Bala lives in an east flat. (4) Bala lives on the floor immediately above Dev, but on the opposite side. (5) Asha lives on the top floor. (6) Chitra lives directly above Esha (same side, next floor up). (7) Bala lives on the top floor. Who lives directly above Gita (same side, next floor up)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Reading a grid (floor and side) and noticing which clues are redundant or fix a single flat.
**Say this in the interview:** "Asha and Bala share the top floor, Bala in the east flat, so Asha is west. Dev is floor 3 west. The remaining clues fit Esha and Gita on floor 1 and Hari on floor 3 east, so Farid is on floor 2 east, directly above Gita."
**Answer:** **Farid**
**Step-by-step reasoning:**
1. Clues 5 and 7 say Asha and Bala are on the top floor (4). Two flats there, so they share it. Bala is east (clue 3), so Asha is west.
2. Clue 4: Dev is on floor 3, on the west side.
3. Esha and Gita are on the same floor (clue 2), so they are on opposite sides. Chitra is above Esha (same side), so Esha is not on floor 4. Hari is on Gita's side with one floor between them.
4. Where can Esha and Gita (one floor, two flats) go? Floor 4 is full, and Chitra must be above Esha, so Esha is not on 4. Floor 3 has only one free flat (Dev has the west one). Floor 2: Chitra above Esha on floor 3 must take the free east flat, so Esha is east and Gita west on floor 2; Hari must then be two floors from Gita on the west side, floor 4 west, which is Asha. Fails. So Esha and Gita are on floor 1.
5. Chitra is directly above Esha, on floor 2. Hari is two floors from Gita on the same side, so floor 3. Floor 3 west is Dev, so Gita is east and Hari is floor 3 east. Then Esha is floor 1 west and Chitra floor 2 west. Farid is the remaining person: floor 2 east.
Building (top to bottom, west | east): 4: Asha | Bala; 3: Dev | Hari; 2: Chitra | Farid; 1: Esha | Gita.
Directly above Gita (floor 1 east) is floor 2 east = Farid.
**Fast method (30 seconds):** Fill the top floor first, then the person tied to it, and the left-over flat is the answer.
**Check:** Brute force over all 40,320 placements: one arrangement fits all seven clues (verified by script).
**Explain simply:**
- Clues 5 and 7 repeat each other in effect; a repeated clue is harmless.
- Farid appears in no clue; he is fixed by elimination.
**Likely follow-ups:** *Who lives opposite Chitra (same floor)?* Farid.
**Common mistakes / traps:** Thinking that Asha and Bala cannot both be on the top floor; forgetting a person with no clue (Farid) still must be placed.

### Q57 ⭐⭐ 🔴 Six people A, B, C, D, E and F sit around a rectangular table: two on the north side (seats N1 in the west and N2 in the east), two on the south side (S1 in the west and S2 in the east), one at the west end (W) and one at the east end (E). Everyone faces the table; N1 faces S1, N2 faces S2 and W faces E. Going around the table, the seats are in the order N1, N2, E, S2, S1, W (and then back to N1). (1) B and F sit next to each other (neighbouring seats going around the table). (2) D and E sit next to each other (neighbouring seats going around the table). (3) A faces B. (4) D and F sit next to each other (neighbouring seats going around the table). (5) F sits in the west half of the table (seat N1, S1 or W). (6) A sits on the north side. Who faces D?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Handling a non-standard layout by numbering seats around the table and finding neighbours.
**Say this in the interview:** "I number the seats around the table. D has two neighbours, and clues 2 and 4 say they are E and F. Then B, F, A tie to the south and west, and the person facing D is C."
**Answer:** **C**
**Step-by-step reasoning:**
1. Seats going around: N1, N2, E-end, S2, S1, W-end. Facing pairs: N1 with S1, N2 with S2, W with E-end.
2. D's two neighbouring seats hold E and F (clues 2 and 4). B is next to F (clue 1), so F's two neighbours are B and D.
3. A is on the north side and faces B, so B is on the south side. If A were at N1, B would be at S1, and F (west half, next to B) would be at W, whose other neighbour is N1, but A is there. Fails. So A is at N2 and B at S2.
4. F is next to B: at E-end or S1. F must be in the west half, so F = S1. F's other neighbour is W, which holds D (the other neighbour of F). D's other neighbour is N1, which is E. C is left: the east end.
Seats: N1 E, N2 A, E-end C, S2 B, S1 F, W D.
D is at the west end, which faces the east end: C.
**Fast method (30 seconds):** When someone has exactly two neighbours named in clues, those two clues fill both of his seats at once.
**Check:** Brute force over all 720 arrangements: exactly one fits all six clues (verified by script).
**Explain simply:**
- "Faces" is defined by the layout: opposite seats across the table.
- In a ring of seats, each seat has exactly two neighbours.
**Likely follow-ups:** *Who sits at the east end?* C, facing D.
**Common mistakes / traps:** Forgetting that the end seats count as neighbours of the corner seats; confusing the person E with the east end seat E.

### Q58 ⭐⭐ 🔴 Eight people A, B, C, D, E, F, G and H sit in a row facing north (so each person's right-hand side is towards the east). (1) B sits at the extreme left end and D sits immediately to the right of B. (2) Exactly 2 persons sit between A and C. (3) H sits immediately to the left of A. (4) F sits immediately to the right of A. (5) E sits immediately to the left of C. (6) G sits at the extreme right end. After the arrangement is found, the persons sitting second from the left end and second from the right end interchange their seats. Who now sits immediately to the left of D?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Solving the base arrangement carefully, then applying a modification step without errors.
**Say this in the interview:** "I find the row first: B D H A F E C G. Then I swap the second from left (D) with the second from right (C), giving B C H A F E D G, so E sits immediately to the left of D."
**Answer:** **E**
**Step-by-step reasoning:**
1. B is at the left end, D next to it (seats 1 and 2). G is at the right end (seat 8).
2. H is immediately left of A and F is immediately right of A, so H, A, F is a block of three.
3. E is immediately left of C, so E, C is a block of two; A and C have 2 between them.
4. Seats 3 to 7 hold H A F (block), E C (block). H A F in seats 3 to 5 and E C in seats 6 to 7: A is seat 4, C is seat 7, with seats 5 and 6 between them: 2 persons. Check the other order: E C in seats 3 and 4, then H A F in 5 to 7: A is seat 6, C is seat 4, 1 person between. Fails.
5. Row: B D H A F E C G.
6. Second from left is D (seat 2), second from right is C (seat 7). Swap: B C H A F E D G.
D is now in seat 7; the person immediately to its left is seat 6 = E.
**Fast method (30 seconds):** Treat chains of "immediately" clues as blocks and slide the blocks into the open seats.
**Check:** Brute force over all 40,320 rows: one satisfies the six clues, and after the swap the left neighbour of D is E (verified by script).
**Explain simply:**
- A block is a group that always stays together.
- After a swap, re-read the final row, do not rely on the old one.
**Likely follow-ups:** *Who sits immediately to the right of D after the swap?* G.
**Common mistakes / traps:** Answering from the original row (that would give D's left as B, wrong); swapping the wrong two seats.

### Q59 ⭐ 🟡 Arrangement puzzles resemble shift rostering and interview scheduling that analysts meet at work. How would you model a roster with "must not be adjacent" and "exactly two days apart" rules in a spreadsheet?
**Asked at:** commonly asked (no company-specific report found); this is a work-link question, not a reported test item.
**What the interviewer is checking:** Whether you can turn verbal rules into numeric formulas, and test them for every pair.
**Say this in the interview:** "I give each person or task a day number, then write each rule as a formula on those numbers: 'not adjacent' is ABS(difference) not equal to 1, and 'exactly two days apart' is a difference of 3 if I mean two days in between. I add a check column and count the failures."
**Answer:** **Model each day as a number (1 to 7) per person, express each rule as an ABS (absolute difference) test, and count how many rules fail.** Formulas below are from memory, not run here; confirm in your Excel or Sheets.
**Explain simply:**
- Table: column A names, column B day number (1 to 7). Rule cells return TRUE or FALSE.
- Not adjacent (Priya in B2, Sam in B3): `=ABS(B2-B3)<>1`.
- Exactly two days apart: decide the meaning first. "Two days in between" is `=ABS(B2-B3)=3`; "difference of two" is `=ABS(B2-B3)=2`. Say which one you used.
- If the week wraps (Sunday next to Monday): `=MIN(MOD(B2-B3,7),MOD(B3-B2,7))<>1`.
- Each person on a different day: `=SUMPRODUCT(1/COUNTIF(B2:B8,B2:B8))=7`.
- A total of failed rules (`=COUNTIF(F2:F10,FALSE)`) must be 0.
**Worked mini-example (verified by script):** Two named people among 7 reviews on 7 days: all schedules 5,040. Not adjacent, no wrap: 5,040 minus 6 adjacent day pairs x 2 orders x 120 = 3,600. Not adjacent, with wrap (7 adjacent pairs): 5,040 minus 7 x 2 x 120 = 3,360. Exactly a difference of 3: 4 day pairs x 2 x 120 = 960. A difference of 2: 5 x 2 x 120 = 1,200.
**Likely follow-ups:** *How would you find a valid roster?* Try Excel Solver (from memory; check it is enabled) or write a short loop in Python.
**Common mistakes / traps:** Not stating what "exactly two days apart" means; forgetting the wrap at the weekend; not checking that every person has a different day.

### Q60 ⭐ 🟡 Your clues are consistent but still allow two different arrangements and the question has a single answer in one of them only. What do you do in a test, and what does it tell you about your reading of the clues?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Calm, honest handling of a flawed or misread puzzle, rather than guessing.
**Say this in the interview:** "I re-read every clue for a missed condition, because a proper puzzle has one arrangement. If two still fit, I check whether both give the same answer; if not, I pick the one that satisfies every clue under the standard reading, and I move on within the time budget."
**Answer:** **Recheck the clues first; if two arrangements truly remain, test which one the question's answer is defined in, choose the option that fits, flag the item, and do not spend more time.** (This is our suggestion, not a research finding.)
**Explain simply:**
- A well-made puzzle has exactly one arrangement. Two arrangements usually mean a misreading (left versus right, "immediately" versus "somewhere", 'between' counting), or a clue you never used.
- Worked example (verified by script): in Q54, reading clue 3 the wrong way round (H on D's left) leaves two arrangements and a wrong answer F. The correct reading leaves one arrangement and the answer E. The extra arrangement was the sign of the misreading.
- If the clues really allow two, check the question: if the asked person has the same answer in both, that answer is safe. If the answer is defined in one arrangement only (the question makes no sense in the other, for example "who sits between X and Y" when they are not neighbours), the puzzle is flawed; choose the answer from the arrangement that obeys all clues in their plainest reading.
- In a timed test: mark it, take the best-supported option, and return if time remains. In an interview, say aloud what you found and ask the interviewer to confirm a clue.
**Likely follow-ups:** *What does it tell you about your reading?* That a clue is probably misread or unused; list the clues you used and check the unused one.
**Common mistakes / traps:** Silently picking one arrangement without saying so; spending ten minutes on one item; assuming the puzzle is wrong before checking your own reading.

### Q61 ⭐ 🔴 8 team leads Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit in a row facing north (so each person's right-hand side is towards the east). (1) Exactly 1 person sits between Asha and Hari. (2) Dev sits somewhere to the left of Gita. (3) Chitra sits second to the right of Esha. (4) Asha and Farid do not sit next to each other. (5) Exactly 3 persons sit between Asha and Gita. (6) Esha sits second to the right of Dev. (7) Exactly 2 persons sit between Farid and Hari. (8) Chitra sits somewhere to the left of Bala. Who sits immediately to the right of Farid?
**Asked at:** commonly asked (no company-specific report found); linear seating puzzles are listed on prep sites for TCS NQT, Infosys and Wipro (prep-site claims, unverified).
**What the interviewer is checking:** Whether you can chain relative-position clues into one block and then test the few places the block can sit.
**Say this in the interview:** "Clues 3 and 6 chain Dev, Esha, Chitra two seats apart, so I treat them as one stretched block and slide it along the row. Only one slide survives all the other clues. Bala is the answer."
**Answer:** **Bala** sits immediately to the right of Farid.
**Step-by-step reasoning:**
1. Seats are numbered 1 to 8 from left (west) to right (east). "To the right" means a higher seat number.
2. Clues 6 and 3 give Dev = x, Esha = x+2, Chitra = x+4. Clue 8 says Bala is right of Chitra, so Chitra cannot be in seat 8; x is 1, 2 or 3.
3. Clue 5 puts Asha and Gita 4 seats apart, clue 1 puts Asha and Hari 2 apart, clue 7 puts Hari and Farid 3 apart, clue 4 keeps Asha and Farid apart.
4. Try x = 2 (Dev 2, Esha 4, Chitra 6) and x = 3 (Dev 3, Esha 5, Chitra 7): in each, Hari and Farid cannot both find free seats and also leave Bala to the right of Chitra, so both fail.
5. Try x = 1 (Dev 1, Esha 3, Chitra 5). Free seats are 2, 4, 6, 7, 8. Asha 2, Gita 6 (4 apart), Hari 4 (2 from Asha), Farid 7 (3 from Hari), Bala 8 (right of Chitra). All clues hold.
```
Seat:  1    2     3     4     5       6     7      8
       Dev  Asha  Esha  Hari  Chitra  Gita  Farid  Bala
```
Unique because the block can only start at seat 1; the brute-force search over all 40,320 orders found exactly this one.
**Fast method (30 seconds):** Find the clues that chain the same people (here Dev, Esha, Chitra), write them as one skeleton "D _ E _ C", and slide it. Use the "somewhere to the right" clue to limit where the skeleton can start.
**Check:** Re-read all 8 clues against the row above: each is true. Verified by script (all 8! orders, one survivor).
**Explain simply:**
- "Second to the right of" means two seats along, not the next one.
- "Exactly 3 persons between" means the seat numbers differ by 4.
- A skeleton with gaps is easier to place than separate names.
**Likely follow-ups:** 1) *Who sits at the left end?* Dev. 2) *Who sits between Hari and Gita?* Chitra.
**Common mistakes / traps:** Treating "second to the right" as adjacent; forgetting that "exactly N between" means a gap of N+1 seats.

### Q62 ⭐ 🔴 8 auditors Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) Chitra sits third to the right of Hari. (2) Asha sits immediately to the right of Hari. (3) Asha sits immediately to the left of Esha. (4) Bala and Farid are neighbours. (5) Gita sits third to the left of Bala. Who sits second to the left of Bala?
**Asked at:** commonly asked (no company-specific report found); circular seating facing the centre is a standard format on prep sites (unverified).
**What the interviewer is checking:** Whether you handle left and right correctly on a circle and build a chain of seats.
**Say this in the interview:** "Facing the centre, right is anticlockwise. Hari, Asha, Esha, Chitra run anticlockwise, then Bala's clues fill the rest. Second to the left of Bala is Dev."
**Answer:** **Dev** sits second to the left of Bala.
**Step-by-step reasoning:**
1. Everyone faces the centre, so right = anticlockwise, left = clockwise (the rule given in the question).
2. Clue 2: Asha is one step anticlockwise of Hari. Clue 3: Esha is one more step anticlockwise (Asha is on Esha's left, so Esha is on Asha's right). Clue 1: Chitra is three steps anticlockwise of Hari. So going anticlockwise: Hari, Asha, Esha, Chitra.
3. Four seats remain, clockwise after Hari: s1, s2, s3, s4, then Chitra. Bala, Farid, Dev, Gita fill them.
4. Clue 5: Gita is three steps clockwise of Bala. That fits only if Bala is s1 and Gita is s4 (any later Bala would push Gita onto an occupied seat).
5. Clue 4: Farid is Bala's neighbour; Bala's other neighbour is Hari, so Farid is s2, leaving Dev in s3.
Clockwise from Hari:
```
Hari -> Bala -> Farid -> Dev -> Gita -> Chitra -> Esha -> Asha -> (back to Hari)
```
Second to the left of Bala = two steps clockwise = Farid, then Dev.
**Fast method (30 seconds):** Build the longest chain of exact clues first (Hari, Asha, Esha, Chitra), then use the "neighbours" and "third to the left" clues to place the leftover four seats.
**Check:** Chitra is 3 anticlockwise of Hari (Asha, Esha, Chitra) yes; Asha right of Hari yes; Esha's left is Asha yes; Gita is 3 clockwise of Bala (Farid, Dev, Gita) yes. Verified by script (all 8! seatings; exactly one pattern up to rotation).
**Explain simply:**
- On a circle there is no first seat, so fix one person and place the rest relative to them. Rotating everybody gives the same seating.
- Anticlockwise is the way a clock hand does NOT move.
- Facing the centre, your right hand points anticlockwise.
**Likely follow-ups:** 1) *Who sits opposite Hari?* Gita (4 seats away). 2) *If everyone faced outside, would the answer change?* Yes, left and right swap, so the same clues describe a different seating.
**Common mistakes / traps:** Using clockwise for "right"; counting "third" as three seats from the wrong person (always count from the person named after "of").

### Q63 ⭐ 🔴 8 HR partners Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit around a circular table, all facing the centre (so a person's right-hand side is the anticlockwise direction). (1) Bala sits immediately to the left of Hari. (2) Asha sits immediately to the right of Gita. (3) Chitra sits second to the left of Hari. (4) Farid sits second to the left of Gita. (5) Bala sits second to the left of Dev. Who sits second to the right of Dev?
**Asked at:** commonly asked (no company-specific report found); circular tables facing the centre are a standard format on prep sites (unverified).
**What the interviewer is checking:** Chaining clues around a circle and keeping clockwise and anticlockwise straight.
**Say this in the interview:** "Facing the centre, left is clockwise. Dev, Hari, Bala, Chitra are consecutive clockwise. Asha, Gita and Esha, Farid fill the other four seats. Second to the right of Dev is Esha."
**Answer:** **Esha** sits second to the right of Dev.
**Step-by-step reasoning:**
1. Everyone faces the centre: left = clockwise, right = anticlockwise.
2. Clue 1: Bala is one step clockwise of Hari. Clue 3: Chitra is two steps clockwise of Hari. Clue 5: Bala is two steps clockwise of Dev, so Dev is two steps anticlockwise of Bala, which is one step anticlockwise of Hari. So clockwise: Dev, Hari, Bala, Chitra.
3. Clue 2: Asha is one step anticlockwise of Gita, so clockwise Asha is followed directly by Gita. Clue 4: Farid is two steps clockwise of Gita.
4. The four remaining seats run clockwise from Chitra: s1, s2, s3, s4, then Dev. Asha, Gita, Esha, Farid fill them.
5. Asha in s1, Gita s2, Esha s3, Farid s4 satisfies clue 4 (Gita, Esha, Farid). Asha in s2 or s3 would put Farid on Dev's seat or beyond, so it fails.
Clockwise:
```
Asha -> Gita -> Esha -> Farid -> Dev -> Hari -> Bala -> Chitra -> (back to Asha)
```
Second to the right of Dev = two steps anticlockwise = Farid, then Esha.
**Fast method (30 seconds):** Convert every clue into "k steps clockwise" and write them as one arrow chain; the leftover seats are then forced.
**Check:** Bala is left of Hari yes; Asha is right of Gita yes; Chitra is 2 clockwise of Hari yes; Farid is 2 clockwise of Gita yes; Bala is 2 clockwise of Dev yes. Verified by script (one pattern up to rotation).
**Explain simply:**
- "Immediately to the left of X" means the next seat clockwise from X (when facing the centre).
- Writing clues as arrows (A -> B = B is one step clockwise of A) avoids left/right slips.
**Likely follow-ups:** 1) *Who is opposite Bala?* Esha (4 seats away in the clockwise list). 2) *Who sits between Farid and Hari?* Dev.
**Common mistakes / traps:** Reading "second to the left of Hari" as the seat two to the left of the page, not two steps clockwise of Hari.

### Q64 ⭐ 🔴 8 managers A, B, C, D, E, F, G and H sit around a circular table. A, D, E and H face the centre and B, C, F and G face outside (away from the centre). 'Right' and 'left' are from each person's own point of view, so for a person facing the centre the right-hand side is the anticlockwise direction, and for a person facing outside it is the clockwise direction. (1) F sits immediately between A and G. (2) B sits second to the left of E. (3) D sits immediately between A and H. (4) D does not sit opposite E. Who sits immediately to the left of B?
**Asked at:** commonly asked (no company-specific report found); circular tables with some people facing outside are a harder variant described on prep sites (unverified).
**What the interviewer is checking:** Applying each person's OWN left and right, and using the last clue to rule out a mirror-image case.
**Say this in the interview:** "G F A D H must sit in a row because F and D are both next to A. Two orientations are possible; clue 4 kills one. B then faces outside, so his left is anticlockwise. That seat is C."
**Answer:** **C** sits immediately to the left of B.
**Step-by-step reasoning:**
1. Facing the centre: right = anticlockwise, left = clockwise. Facing outside: right = clockwise, left = anticlockwise.
2. Clue 1 (F between A and G) and clue 3 (D between A and H): A has F and D as both neighbours, so five seats in a row read G, F, A, D, H, one way round or the other. Three seats remain for B, C, E.
3. Orientation 1, clockwise G F A D H then x1, x2, x3. E faces the centre, so "B second to the left of E" means B is two steps clockwise of E: E = x1, C = x2, B = x3. Clue 4: D is not opposite E; D is opposite B here, so it holds.
4. Orientation 2, clockwise H D A F G then y1, y2, y3. Clue 2 forces E = y1, C = y2, B = y3, but then D sits opposite E, which clue 4 forbids. Orientation 2 fails.
Clockwise (the survivor, rotated to start at A):
```
A(in) -> D(in) -> H(in) -> E(in) -> C(out) -> B(out) -> G(out) -> F(out) -> (back to A)
```
5. B faces outside, so his left is anticlockwise: the seat before B in the list, which is C.
**Fast method (30 seconds):** Anchor on the person named twice (A), build the row of five, and treat the final negative clue as the tie-breaker between the two mirror cases.
**Check:** F is between A and G yes; D between A and H yes; B is two clockwise of E (E, C, B) yes; D (seat 2) and E (seat 4) are not opposite yes. Verified by script (one pattern up to rotation).
**Explain simply:**
- "Left" depends on which way the person faces. The same neighbour can be left for one person and right for another.
- "Opposite" on 8 seats means 4 seats away.
**Likely follow-ups:** 1) *Who sits immediately to the right of B?* G (B faces outside, right is clockwise). 2) *Why is clue 4 needed?* Without it, the mirror case also fits and the answer would be ambiguous.
**Common mistakes / traps:** Using the centre-facing rule for someone who faces outside, which would give G instead of C.

### Q65 ⭐ 🔴 7 candidates Asha, Bala, Chitra, Dev, Esha, Farid and Gita sit around a circular table. Chitra, Dev, Esha and Farid face the centre and Asha, Bala and Gita face outside (away from the centre). 'Right' and 'left' are from each person's own point of view, so for a person facing the centre the right-hand side is the anticlockwise direction, and for a person facing outside it is the clockwise direction. (1) Gita sits third to the left of Asha. (2) Farid sits second to the left of Bala. (3) Bala sits third to the right of Esha. (4) Gita sits second to the right of Dev. Who sits immediately to the left of Esha?
**Asked at:** commonly asked (no company-specific report found); mixed-facing circular tables are described on prep sites (unverified).
**What the interviewer is checking:** Translating "third to the left" into the right direction for each speaker's facing, then pinning seats on a 7-seat circle.
**Say this in the interview:** "I fix Gita, place Asha and Dev from her, then test where Bala can go; only one spot fits. Reading it off, Esha faces the centre, so her left is clockwise, and that seat is Chitra."
**Answer:** **Chitra** sits immediately to the left of Esha.
**Step-by-step reasoning:**
1. Centre-facing (Chitra, Dev, Esha, Farid): left = clockwise, right = anticlockwise. Outside-facing (Asha, Bala, Gita): left = anticlockwise, right = clockwise.
2. Put Gita at seat 0 and number seats clockwise 0 to 6.
3. Clue 1: Gita is 3 anticlockwise of Asha, so Asha is at seat 3. Clue 4: Gita is 2 anticlockwise of Dev, so Dev is at seat 2.
4. Clue 3: Bala is 3 anticlockwise of Esha, so Esha = Bala + 3. Clue 2: Farid is 2 anticlockwise of Bala, so Farid = Bala - 2. Free seats are 1, 4, 5, 6.
5. Bala 1 gives Esha 4 and Farid 6, both free, so it works. Bala 4, 5 or 6 each push Esha or Farid onto an occupied seat. Chitra takes seat 5.
Clockwise:
```
Gita(out) -> Bala(out) -> Dev(in) -> Asha(out) -> Esha(in) -> Chitra(in) -> Farid(in) -> (back to Gita)
```
Esha faces the centre, so her left is clockwise: Chitra.
**Fast method (30 seconds):** Number the seats 0 to 6 and turn every clue into a formula (X = Y + 3 and so on); then test the one unknown (Bala) against the free seats.
**Check:** Gita is 3 anticlockwise of Asha (Dev, Bala, Gita counted back from Asha) yes; Farid is 2 anticlockwise of Bala yes; Bala is 3 anticlockwise of Esha (Asha, Dev, Bala) yes; Gita is 2 anticlockwise of Dev (Bala, Gita) yes. Verified by script (one pattern up to rotation).
**Explain simply:**
- Mod arithmetic on a circle: seat 7 is the same as seat 0, so "3 steps past seat 5" lands on seat 1 (7 seats).
- The speaker's facing decides the direction, not the order of the names in the sentence.
**Likely follow-ups:** 1) *Who sits immediately to the right of Esha?* Esha faces the centre, so right is anticlockwise: Asha. 2) *Does a 7-seat circle have an exact opposite?* No, 7 is odd.
**Common mistakes / traps:** Using one direction rule for everyone; mixing up "A is third to the left of B" with "B is third to the left of A".

### Q66 ⭐ 🔴 8 trainers Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari sit around a circular table. Dev, Esha, Gita and Hari face the centre and Asha, Bala, Chitra and Farid face outside (away from the centre). 'Right' and 'left' are from each person's own point of view, so for a person facing the centre the right-hand side is the anticlockwise direction, and for a person facing outside it is the clockwise direction. (1) Chitra sits immediately to the right of Bala. (2) Esha sits third to the right of Dev. (3) Asha sits immediately between Esha and Hari. (4) Bala sits third to the left of Hari. (5) Farid sits second to the left of Hari. Who sits third to the right of Hari?
**Asked at:** commonly asked (no company-specific report found); mixed-facing circular tables appear on prep sites (unverified).
**What the interviewer is checking:** Using each person's own facing and anchoring on the person with the most clues (Hari).
**Say this in the interview:** "Hari faces the centre and appears in three clues, so I fix him and place Farid, Bala and Chitra clockwise from him, then slot Asha, Esha, Dev and Gita. Third to Hari's right is Gita."
**Answer:** **Gita** sits third to the right of Hari.
**Step-by-step reasoning:**
1. Centre-facing (Dev, Esha, Gita, Hari): left = clockwise. Outside-facing (Asha, Bala, Chitra, Farid): right = clockwise.
2. Hari at seat 0, seats numbered clockwise. Clue 5: Farid is 2 clockwise of Hari, so Farid = 2. Clue 4: Bala is 3 clockwise of Hari, so Bala = 3. Clue 1: Bala faces outside, so his right is clockwise and Chitra = 4.
3. Clue 3: Asha is a neighbour of both Hari and Esha, so Asha is seat 1 or 7. Seat 1 would put Esha at 0 or 2, both taken. So Asha = 7 and Esha = 6.
4. Clue 2: Esha is 3 anticlockwise of Dev, so Dev = 6 + 3 = 9, which is seat 1. Gita takes seat 5.
Clockwise:
```
Hari(in) -> Dev(in) -> Farid(out) -> Bala(out) -> Chitra(out) -> Gita(in) -> Esha(in) -> Asha(out) -> (back to Hari)
```
5. Hari faces the centre, so his right is anticlockwise: Asha, Esha, Gita. Third to the right is Gita.
**Fast method (30 seconds):** Anchor on the most-mentioned person, fix three clockwise seats at once, then use the "between" clue to choose among two seats for Asha.
**Check:** Chitra is right of Bala yes; Esha is 3 anticlockwise of Dev (Hari, Asha, Esha) yes; Asha between Esha and Hari yes; Bala is 3 clockwise of Hari yes; Farid is 2 clockwise of Hari yes. Verified by script (one pattern up to rotation).
**Explain simply:**
- Each clue is a small equation on seat numbers; the one person in many clues gives you the free anchor.
- Facing outside flips left and right compared with facing the centre.
**Likely follow-ups:** 1) *Who sits immediately to the left of Asha?* Asha faces outside, left is anticlockwise: Esha. 2) *Who sits opposite Hari?* Chitra.
**Common mistakes / traps:** Treating Asha (outside-facing) like the centre-facing people when moving "between" her neighbours.

### Q67 ⭐ 🔴 Four men (Asha, Chitra, Dev and Farid) and four women (Bala, Esha, Gita and Hari) sit around a circular table facing the centre (so a person's right-hand side is the anticlockwise direction), alternating so that no two men and no two women sit next to each other. (1) Asha sits immediately to the left of Esha. (2) Gita sits immediately between Asha and Dev. (3) Bala sits immediately to the left of Chitra. Who sits opposite Dev?
**Asked at:** commonly asked (no company-specific report found); alternating-gender circular puzzles are common on prep sites (unverified).
**What the interviewer is checking:** Using the alternating rule to fill seats and read left or right correctly.
**Say this in the interview:** "Men and women alternate, so Esha, Asha, Gita, Dev run clockwise. Chitra and Bala are a pair, and the gender pattern fixes the rest. Opposite Dev is Farid."
**Answer:** **Farid** sits opposite Dev.
**Step-by-step reasoning:**
1. Everyone faces the centre: left = clockwise, right = anticlockwise.
2. Clue 1: Asha is immediately to the left of Esha, so Asha is one step clockwise of Esha.
3. Clue 2: Gita is between Asha and Dev. Asha's other neighbour is Esha, so Gita is on the clockwise side. Clockwise: Esha, Asha, Gita, Dev.
4. The four remaining seats run clockwise after Dev. They alternate: woman, man, woman, man. The women left are Bala and Hari; the men are Chitra and Farid.
5. Clue 3: Bala is one step clockwise of Chitra. Only the seats (man, woman) = (second, third) fit; Chitra in the last seat would put Bala on Esha's seat. So seats: Hari, Chitra, Bala, Farid.
Clockwise:
```
Asha -> Gita -> Dev -> Hari -> Chitra -> Bala -> Farid -> Esha -> (back to Asha)
```
Opposite means 4 seats away: Dev (3rd) and Farid (7th).
**Fast method (30 seconds):** Write the gender pattern M W M W M W M W first, so every unknown seat is already "man" or "woman"; then each clue only has two seats to choose from.
**Check:** Alternation holds yes; Asha is left of Esha yes; Gita sits between Asha and Dev yes; Bala is left of Chitra yes. Verified by script (one pattern up to rotation).
**Explain simply:**
- Alternating groups halve the choices: a man can only go in a "man seat".
- "Opposite" on a circle of 8 is half way round.
**Likely follow-ups:** 1) *Who sits opposite Gita?* Bala. 2) *Who are Hari's neighbours?* Dev and Chitra.
**Common mistakes / traps:** Forgetting the alternation rule when two seats look possible; mixing up left and right in the "immediately to the left" clues.

### Q68 ⭐ 🔴 8 boxes coloured Red, Blue, Green, Yellow, Black, White, Orange and Grey are stacked one on top of another in a single pile. (1) The Blue box is neither at the top nor at the bottom. (2) The Blue and White boxes are not touching. (3) Exactly 2 boxes lie between the Green and White boxes. (4) The Yellow box is 3 places above the Grey box (so 2 boxes lie between them). (5) The Blue and Black boxes are not touching. (6) The Red box is somewhere below the White box. (7) The Orange box is directly between the Green and Grey boxes. (8) Exactly 1 box lies between the Yellow and Orange boxes. Which box is second from the top?
**Asked at:** commonly asked (no company-specific report found); stack and floor-arrangement puzzles are listed on prep sites (unverified).
**What the interviewer is checking:** Merging clues into one block and doing a short case check.
**Say this in the interview:** "Yellow, Green, Orange, Grey form a block of four, since Grey is 3 below Yellow and Orange sits between Green and Grey. I slide the block and test White's two possible spots. Only one case survives: Black is second from the top."
**Answer:** **Black** is second from the top.
**Step-by-step reasoning:**
1. Number the places 1 (top) to 8 (bottom). Clue 4: Grey = Yellow + 3. Clue 7: Orange touches both Green and Grey. Clue 8: Orange is 2 places from Yellow. Orange = Yellow + 2 (next to Grey), so Green = Yellow + 1. Block: Yellow, Green, Orange, Grey in places p to p+3.
2. Clue 3: White is 2 boxes away from Green, so White is at p+4 or p-2.
3. White at p+4: p = 1 leaves Blue and Black adjacent in places 7 and 8 or Blue touching White; p = 2 and p = 3 leave no legal place for Blue; p = 4 puts White at the bottom and Red cannot be below it. All fail.
4. White at p-2: p = 4 and p = 5 leave Blue only a place touching White. p = 3 works: White 1, free places 2, 7, 8. Blue cannot be at an end or touch White, so Blue = 7. Black cannot touch Blue, so Black = 2, and Red = 8 (below White).
```
1 White
2 Black
3 Yellow
4 Green
5 Orange
6 Grey
7 Blue
8 Red
```
Unique: brute force over all 40,320 orders left exactly one.
**Fast method (30 seconds):** Combine the "touching" and "between" clues into one block of four, then use the "not touching" and "not at an end" clues on Blue (the most restricted box) to cut cases.
**Check:** Blue is 7th, not at an end yes; Blue not touching White (1st) yes; 2 boxes between Green (4th) and White (1st) yes; Yellow 3 above Grey yes; Blue and Black (2nd) not touching yes; Red below White yes; Orange between Green and Grey yes; 1 box between Yellow and Orange yes. Verified by script.
**Explain simply:**
- "N boxes between" means the places differ by N+1.
- Start with the most restricted item (Blue has three "not" clues).
**Likely follow-ups:** 1) *Which box is at the bottom?* Red. 2) *Which box is exactly in the middle two places?* Green (4th) and Orange (5th).
**Common mistakes / traps:** Reading "3 places above" as 3 boxes between rather than 2 between.

### Q69 ⭐ 🔴 8 new joiners Asha, Bala, Chitra, Dev, Esha, Farid, Gita and Hari join the company in 8 consecutive months starting January, one per month. (1) Gita joins in neither January nor August. (2) Farid joins the month after Esha. (3) Asha joins 3 months after Chitra. (4) Bala and Gita do not join in consecutive months. (5) Exactly 3 months separate Chitra and Esha. (6) Hari joins 2 months after Bala. (7) Hari joins earlier in the year than Dev. Who joins in May?
**Asked at:** commonly asked (no company-specific report found); month and weekday ordering puzzles are common on prep sites (unverified).
**What the interviewer is checking:** Turning "k months after" into arithmetic on month numbers and pruning cases quickly.
**Say this in the interview:** "Number the months 1 to 8. Chitra and Esha are 4 months apart, with Asha 3 after Chitra and Farid 1 after Esha. Testing Chitra's month gives only February; May is Asha."
**Answer:** **Asha** joins in May.
**Step-by-step reasoning:**
1. Months 1 (January) to 8 (August). Clue 5: exactly 3 months between Chitra and Esha means their numbers differ by 4.
2. Case Chitra before Esha: Chitra = c, Esha = c+4, Farid = c+5, Asha = c+3. So c is at most 3 (Farid must be 8 or less).
 - c = 1: free months 2, 3, 7, 8 have no pair 2 apart for Bala and Hari. Fail.
 - c = 3: free months 1, 2, 4, 5. Bala 2, Hari 4 is the only pair 2 apart; Dev must be after Hari, so Dev = 5 and Gita = 1, which breaks clue 1. Fail.
 - c = 2: free months 1, 3, 4, 8. Bala 1, Hari 3 (clue 6), then Gita not in 8 (clue 1) so Gita = 4 and Dev = 8. All clues hold.
3. Case Esha before Chitra: Esha 1, Farid 2, Chitra 5, Asha 8; free 3, 4, 6, 7. Bala 4, Hari 6, Gita 3 is next to Bala (clue 4). Fail.
```
Jan Bala | Feb Chitra | Mar Hari | Apr Gita | May Asha | Jun Esha | Jul Farid | Aug Dev
```
**Fast method (30 seconds):** Pick the pair with the tightest rule (Chitra and Esha 4 apart) and run through its few positions; the other "k after" clues then place people almost mechanically.
**Check:** Gita in April (not Jan or Aug) yes; Farid (Jul) is the month after Esha (Jun) yes; Asha (May) is 3 after Chitra (Feb) yes; Bala (Jan) and Gita (Apr) not consecutive yes; Hari (Mar) is 2 after Bala yes; Hari before Dev yes. Verified by script (all 40,320 orders, one survivor).
**Explain simply:**
- "A joins k months after B" means number(A) = number(B) + k.
- "Exactly 3 months between" means a gap of 4 in the numbers.
**Likely follow-ups:** 1) *Who joins in March?* Hari. 2) *Who joins just before Asha?* Gita.
**Common mistakes / traps:** Using a gap of 3 instead of 4 for "exactly 3 months separate".

### Q70 ⭐ 🔴 8 people A, B, C, D, E, F, G and H sit in two parallel rows of 4. Row 1 faces south and row 2 faces north, so each person in one row sits directly opposite (faces) exactly one person in the other row. 'Right' and 'left' are from each person's own point of view. (1) F and H sit in different rows. (2) A faces E. (3) B faces H. (4) F sits immediately to the right of G. (5) F sits in row 1. (6) A sits immediately to the left of C. (7) E sits at one end of a row. Who faces G?
**Asked at:** commonly asked (no company-specific report found); two-row facing puzzles are listed on prep sites (unverified).
**What the interviewer is checking:** Handling opposite facing rows and remembering that left and right flip between the rows.
**Say this in the interview:** "Row 1 faces south, so its right is west; row 2 faces north, so its right is east. G is in row 1 with F beside him, and the other clues fill the rest. G faces D."
**Answer:** **D** faces G.
**Step-by-step reasoning:**
1. Number the columns 1 to 4 from west to east. Row 1 faces south (right = west); row 2 faces north (right = east, left = west).
2. Clue 5: F is in row 1. Clue 1: H is in row 2. Clue 3: B faces H, so B is in row 1. Clue 4: F is immediately right of G in the same row, so G is also in row 1. Row 1 holds F, G, B plus one more.
3. Clue 2: A and E are in opposite rows. Clue 6: A and C are in the same row. If A were in row 1, row 1 would need A, C, F, G, B = 5 people. So A and C are in row 2, E is in row 1.
4. Row 1 is E, F, G, B in some order. Clue 4: F (right = west) sits just west of G. Clue 7: E is at an end. Options: E F G B, E B F G, B F G E.
 - B F G E: A faces E in column 4 and A needs C east of A (A is on C's left, row 2 left is west). No room. Fail.
 - E B F G: H faces B in column 2, but A faces E in column 1 and C must be in column 2. Clash. Fail.
 - E F G B: A column 1, C column 2, H column 4 (faces B), D column 3.
```
West  ->  East
Row 1 (faces south):  E   F   G   B
Row 2 (faces north):  A   C   D   H
```
G (column 3) faces D (column 3).
**Fast method (30 seconds):** Start with the clues that name a row (F row 1, H row 2), then use "faces" clues to copy columns, and test only the two or three orders of the row that has the end clue.
**Check:** F and H in different rows yes; A faces E yes; B faces H yes; F is just right of G (west of G, row 1) yes; F in row 1 yes; A just left of C (west) yes; E at an end yes. Verified by script (all assignments; one survivor).
**Explain simply:**
- People who face opposite ways have opposite left and right. Row 1's right is west; row 2's is east.
- "Faces" means same column, other row.
**Likely follow-ups:** 1) *Who faces C?* F. 2) *Who is to the immediate right of D?* In row 2 facing north, right is east: H.
**Common mistakes / traps:** Using east as "right" for both rows, which gives the wrong order for F and G.

### Q71 ⭐ 🔴 In which months of 2026 does the 13th fall on a Friday? (1 January 2026 is a Thursday.)
**Asked at:** commonly asked (no company-specific report found); calendar and day-of-week problems are standard aptitude topics (prep-site claim, unverified).
**What the interviewer is checking:** Working with days modulo 7 and month lengths.
**Say this in the interview:** "The 13th is 12 days after the 1st, and 12 leaves a remainder of 5 when divided by 7. So the 13th is a Friday exactly when the 1st is a Sunday. I list which months start on a Sunday: February, March, November."
**Answer:** **February, March and November 2026.**
**Step-by-step reasoning:**
1. From the 1st to the 13th is 12 days. 12 = 7 + 5, so the 13th falls 5 days after the weekday of the 1st.
2. Friday is 5 days after Sunday, so the 13th is Friday exactly when the 1st is Sunday.
3. 1 January is a Thursday. Each month moves the 1st forward by (days in month) mod 7. January has 31 days (31 mod 7 = 3), so 1 February is Thursday + 3 = Sunday. Good.
4. February 2026 has 28 days (not a leap year), mod 7 = 0, so 1 March is Sunday too. March has 31 (3), so 1 April is Wednesday. Continuing: 1 May Friday, 1 June Monday, 1 July Wednesday, 1 August Saturday, 1 September Tuesday, 1 October Thursday, 1 November Sunday, 1 December Tuesday.
```
1st is Sunday in: Feb, Mar, Nov  ->  13th is Friday in: Feb, Mar, Nov
```
**Fast method (30 seconds):** Only the 1st's weekday matters; the 13th is Friday if the 1st is Sunday. Add 3 for 31-day months, 2 for 30-day months, 0 for a 28-day February.
**Check:** Python's calendar gave 13 February, 13 March and 13 November 2026 as Fridays. Verified by script.
**Explain simply:**
- "Modulo 7" means keep only the remainder after dividing by 7, because weekdays repeat every 7 days.
- A 31-day month pushes the next 1st forward by 3 weekdays (31 = 28 + 3).
**Likely follow-ups:** 1) *Which month in 2027 has a Friday the 13th?* August only (checked by script). 2) *How many Friday the 13ths are possible in a year?* From 1 to 3 (from memory, not run here; 2026 has exactly 3).
**Common mistakes / traps:** Forgetting that February has 28 days in 2026 (it is not a leap year); counting 13 days instead of 12 days after the 1st.

### Q72 ⭐ 🔴 In how many ways can 8 distinct people sit in a row of 8 chairs if three particular people, X, Y and Z, must occupy three consecutive chairs (in any order among themselves)?
**Asked at:** commonly asked (no company-specific report found); the "keep some people together" counting idea is standard on prep sites (unverified).
**What the interviewer is checking:** The "glue them into one block" counting trick.
**Say this in the interview:** "Treat X, Y, Z as one block. Then there are 6 things to arrange, which is 6 factorial, 720 ways. Inside the block the three can be ordered 3 factorial, 6 ways. So 720 times 6 is 4,320."
**Answer:** **4,320 ways.**
**Step-by-step reasoning:**
1. Glue X, Y, Z into one block. The row now has the block plus 5 other people = 6 items.
2. 6 items can be arranged in 6! = 720 ways. (n! means n times n-1 times ... times 1.)
3. Inside the block, X, Y, Z can be ordered 3! = 6 ways.
4. Multiply, since each outer arrangement pairs with each inner order: 720 x 6 = 4,320.
**Fast method (30 seconds):** "Together" means glue, then multiply by the inside arrangements.
**Check:** Counted by brute force over all 40,320 seatings: 4,320 have X, Y, Z in three consecutive chairs. Verified by script.
**Explain simply:**
- Factorial n! is the number of ways to order n different things.
- Multiplication rule: independent choices multiply.
**Likely follow-ups:** 1) *If they must sit in the order X, Y, Z?* 6! = 720 (verified by script). 2) *If they must NOT all sit together?* 40,320 - 4,320 = 36,000.
**Common mistakes / traps:** Forgetting the 3! inside the block (answering 720), or using 7! x 3! by miscounting the units.

### Q73 ⭐ 🔴 In how many ways can 6 distinct people sit in a row of 6 chairs if two particular people, A and B, must both avoid the two end chairs?
**Asked at:** commonly asked (no company-specific report found); restricted-position counting is standard on prep sites (unverified).
**What the interviewer is checking:** The "place the restricted people first" counting rule.
**Say this in the interview:** "Seat the two restricted people first. They must use the 4 middle chairs: 4 choices for A, 3 for B, which is 12. The other 4 people fill the remaining 4 chairs in 4 factorial, 24 ways. 12 times 24 is 288."
**Answer:** **288 ways.**
**Step-by-step reasoning:**
1. The two end chairs are banned for A and B, leaving the 4 middle chairs.
2. A can take any of the 4 middle chairs: 4 ways. B then takes one of the remaining 3 middle chairs: 3 ways. 4 x 3 = 12.
3. The 4 other people fill the 4 chairs left (including both ends): 4! = 24 ways.
4. Total = 12 x 24 = 288.
**Fast method (30 seconds):** Place the fussy people first; the unrestricted people fill whatever is left.
**Check:** Brute-force enumeration of all 720 seatings found 288 with neither A nor B at an end. Verified by script.
**Explain simply:**
- Place the most restricted items first; otherwise you must subtract overlapping cases.
- The product rule: if one task has 12 ways and the next has 24, together there are 12 x 24.
**Likely follow-ups:** 1) *If A and B must sit next to each other?* 5! x 2 = 240 (verified by script). 2) *With 7 people and 7 chairs, A and B avoiding the ends?* 5 x 4 x 5! = 2,400 (verified by script).
**Common mistakes / traps:** Placing the others first, then trying to fit A and B; or giving A all 6 chairs.

### Q74 ⭐ 🔴 Three married couples sit around a circular table with 6 equally spaced chairs so that men and women alternate and no husband sits next to his own wife. How many different seatings are possible? (Rotations are the same seating; mirror images are different.)
**Asked at:** commonly asked (no company-specific report found); this is the classic "couples around a table" counting problem (known as the ménage problem), a differentiator rather than a reported analyst question.
**What the interviewer is checking:** Fixing the circle's symmetry and counting a constrained pattern without double counting.
**Say this in the interview:** "I fix one husband to remove the rotation. The other two husbands can be arranged in 2 ways. Each wife then has only one seat that is not next to her husband, so the women are forced. The answer is 2."
**Answer:** **2 seatings.**
**Step-by-step reasoning:**
1. Fix husband H1 in one chair; this removes rotations (turning everyone round the table gives the same seating). The men then sit in chairs 1, 3, 5 and the women in 2, 4, 6.
2. The other two husbands can fill chairs 3 and 5 in 2! = 2 ways.
3. Each woman's seat is between two men. A wife must not sit in either of the two chairs next to her husband. That leaves exactly one allowed seat (the chair between the other two men). So the women's seating is forced.
4. Total = 2 x 1 = 2.
```
Seating 1 (clockwise): H1, W2, H3, W1, H2, W3
Seating 2 (clockwise): H1, W3, H2, W1, H3, W2   (mirror image of seating 1)
```
**Fast method (30 seconds):** Fix one person, then count how many choices each woman has; here each wife has only one legal seat.
**Check:** Brute force over all 720 arrangements found 12 valid seatings with labelled chairs, which is 12 / 6 rotations = 2. Verified by script.
**Explain simply:**
- Rotations count as one seating, so fix one person to remove them.
- The two seatings are mirror images of each other; the question says mirror images are different, so both count.
**Likely follow-ups:** 1) *If mirror images counted as the same?* Then 1. 2) *With 4 couples?* 12 seatings up to rotation (verified by script).
**Common mistakes / traps:** Counting 3! x 3! = 36 or forgetting to divide out rotations (12 labelled-chair seatings, not 2).

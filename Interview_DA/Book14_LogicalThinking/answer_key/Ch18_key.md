# Chapter 18 answer key: Puzzles with Floors, Boxes, Days, Months and Schedules

Every puzzle (Q1 to Q3, Q7 to Q13, Q16 to Q20, Q23 to Q25 and worked examples 1, 2 and 5) was solved by brute force: all arrangements were generated and filtered by every clue, and in each case exactly one arrangement survived (Q4 to Q6, Q14, Q15, Q21 and Q22 were recomputed from calendars, clocks or a schedule search). The schedule answers (Q15, Q22, example 4, scenario 1) were checked by trying every task order and every assignment of tasks to workers. The calendar answers (Q4, Q14, Q21, example 3, scenario 2) were recomputed with a date library. In the reasoning below, "floor 1" is the lowest floor.

## Self-check answers

1. "A is directly above B" means A is exactly one floor higher than B. That is a special case of "A is above B", so **yes**, directly above always implies above. It does **not** work the other way: "A is above B" allows any gap (A could be 3 floors higher), so it does not mean directly above.
2. 10 days is 1 full week (7 days) plus 3 extra days. Wednesday plus 3 is Thursday, Friday, Saturday. **Saturday**.
3. The tasks are independent, so with two people one takes the 3-hour task and the other takes the 5-hour task at the same time. The job ends when the slower one ends: **5 hours** (one person alone would need 8 hours).

## Practice answers

**Q1** 🟢 Clue 1 puts Admin on floor 1. Floors 2, 3 and 4 are left for Payroll, Hiring and Training. Clue 3 ties Payroll and Hiring into a block (Payroll directly below Hiring), which fits floors 2 and 3, or floors 3 and 4. If the block is on floors 2 and 3, Training would be on floor 4, above Hiring, which breaks clue 2 (Hiring must be higher than Training). So the block is on floors 3 and 4 (Payroll 3, Hiring 4) and Training is on floor 2. Check: Hiring (4) is higher than Training (2); Payroll (3) is directly below Hiring (4). **Training is on floor 2.** (Full order: Admin 1, Training 2, Payroll 3, Hiring 4.)

**Q2** 🟢 Contracts are on shelf 5 (clue 1). Leave forms are on shelf 2 (clue 2). Offer letters are directly above Leave forms, so on shelf 3 (clue 3). Shelves 1 and 4 are left for Payslips and Exit papers. Clue 4 says Payslips are higher than Exit papers, so Payslips take shelf 4 and Exit papers take shelf 1. **Exit papers are on shelf 1.**

**Q3** 🟢 Grid of items against boxes. The diary cannot be in green (clue 2) or blue (clue 4), so the diary is in the **red** box. The ribbon cannot be red (clue 1), and red is now taken anyway. The stapler cannot be in blue (clue 3) and cannot be in red (taken), so the stapler is in green. The ribbon takes the last box, blue. Check: ribbon not red, diary not green, stapler not blue, diary not blue. All hold. **The blue box holds the ribbon.**

**Q4** 🟢 Counting 10 days forward from Tuesday: 10 is 1 week plus 3 days, so move 3 weekdays: Wednesday, Thursday, Friday. The due day is Friday. The holiday is the day before the due day, which is **Thursday**.

**Q5** 🟢 "7 months after April" means counting on from May: May 1, June 2, July 3, August 4, September 5, October 6, November 7. Priya joined in November. Three months after November: December, January, February. Her probation ends in **February** (the year changes after December).

**Q6** 🟢 Add the durations step by step. 9:20 plus 25 minutes is 9:45 (end of packing). Plus 15 minutes is 10:00 (end of labelling). Plus 10 minutes is 10:10 (end of the break). Plus 40 minutes is 10:50. Total duration is 25 + 15 + 10 + 40 = 90 minutes, and 9:20 plus 90 minutes is 10:50. **10:50.**

**Q7** 🟢 Kabir is not on Wednesday (clue 3). Lata is not on Monday (clue 2). Meera is before Kabir (clue 1), so Kabir cannot be on Monday, which leaves Tuesday for Kabir (Wednesday is barred). Meera, being before Kabir, is on Monday. Lata takes Wednesday. Check: Meera (Mon) is before Kabir (Tue); Lata not Monday; Kabir not Wednesday. **Lata is interviewed on Wednesday.**

**Q8** 🟢 Chain the clues: S is heavier than P (clue 3), P is heavier than Q (clue 1), Q is heavier than R (clue 2). That gives one unbroken chain S > P > Q > R. **S, P, Q, R** (heaviest to lightest).

**Q9** 🟡 Stores is directly above Accounts (clue 3), so Accounts is directly below Stores. IT must be adjacent to Stores (clue 1): that is either the floor above Stores or the floor below Stores. The floor below Stores is Accounts, so IT is directly above Stores. Legal is adjacent to IT (clue 4): the floor below IT is Stores, so Legal is directly above IT. This builds a block of four from the bottom: Accounts, Stores, IT, Legal. Sales is higher than IT (clue 2), so Sales cannot be below the block; the block occupies floors 1 to 4 and Sales takes floor 5. Order: Accounts 1, Stores 2, IT 3, Legal 4, Sales 5. All clues check. **Floor 1: Accounts. Floor 4: Legal.**

**Q10** 🟡 Sales is directly above HR (clue 4). Stores is adjacent to Sales (clue 1); the floor below Sales is HR, so Stores is directly above Sales. This gives a block going up: HR, Sales, Stores on floors k, k+1, k+2. Accounts is below HR (clue 5), so k is at least 2. Try each k.
- k = 4 would need floors 4 to 6 for the block, leaving no floor above HR for Legal (clue 2). Impossible.
- k = 3: block on floors 3 to 5. Legal must be above HR, so Legal is on floor 6, which is adjacent to Stores on floor 5. That breaks clue 3. Impossible.
- k = 2: block on floors 2 to 4, Accounts on floor 1. Floors 5 and 6 are left for Legal and IT. Legal cannot be on floor 5 (adjacent to Stores on floor 4, clue 3), so Legal is on 6 and IT on 5.
Check: Accounts 1, HR 2, Sales 3, Stores 4, IT 5, Legal 6. All five clues hold. **IT is on floor 5.**

**Q11** 🟡 Clue 5: blue holds the cables. Clue 4: the cables box is immediately left of the red box. Clue 1: the red box is immediately left of the mugs box. So three boxes in a row, left to right: blue (cables), red, mugs-box. Blue is at position 1 or 2.
- If blue is at 2: red at 3, mugs-box at 4. The mugs box must be next to the green box (clue 2), so green would be at 3, but red is there. Impossible.
- So blue is at 1, red at 2, and the mugs box is at position 3. The badges box is next to blue (clue 3), so badges are at position 2 (the red box). The files are at position 4. The mugs box (position 3) must be next to green (clue 2), so green is at position 4 (position 2 is red). The mugs box at position 3 is therefore the remaining colour, yellow.
Final: 1 blue cables, 2 red badges, 3 yellow mugs, 4 green files. **The yellow box holds the mugs, and the box at position 4 is green.**

**Q12** 🟡 Try each box as the key box and count how many labels are true (exactly one must be).
- Key in box 1: label 1 false (key is not in 2 or 3), label 2 false, label 3 true, label 4 true. Two true. No.
- Key in box 2: label 1 true, label 2 true, label 3 true, label 4 false. Three true. No.
- Key in box 3: label 1 true, label 2 false, label 3 false, label 4 true. Two true. No.
- Key in box 4: label 1 false, label 2 false, label 3 true ("not in this box" is true because the key is elsewhere), label 4 false. Exactly one true. Yes.
Assumption: exactly one box holds the key, as the question says. **The key is in box 4.**

**Q13** 🟡 Dosa is the day right after Upma (clue 2). Upma and Paratha are on consecutive days (clue 1); the day after Upma is taken by Dosa, so Paratha must be the day **before** Upma. This gives Paratha, Upma, Dosa in three consecutive days. Idli is next to Paratha (clue 3); the day after Paratha is Upma, so Idli is the day before Paratha. Poha is next to Idli (clue 4); the day after Idli is Paratha, so Poha is the day before Idli. The full chain: Poha, Idli, Paratha, Upma, Dosa, which exactly fills Monday to Friday. Monday Poha, Tuesday Idli, Wednesday Paratha, Thursday Upma, Friday Dosa. **Wednesday: Paratha.**

**Q14** 🟡 Months in July to December with 31 days: July, August, October, December. Check the months on either side.
- July: before it is June (30 days, good), after it is August (31 days, fails).
- August: before it is July (31 days), fails.
- October: before it is September (30), after it is November (30). Passes.
- December: before it is November (30), after it is January (31). Fails.
The month is **October**. If 1 October is a Wednesday, 31 October is 30 days later. 30 is 4 weeks plus 2 days, so move 2 weekdays: Thursday, Friday. The last day is a **Friday**.

**Q15** 🟡 One person: 2 + 3 + 2 + 4 + 3 = **14 hours**. For two people, find the waiting chains. A then C then E takes 2 + 2 + 3 = 7 hours; A then D takes 6; B then E takes 6. The longest chain (critical path) is 7, so nobody can do better than 7 hours. Is 7 reachable with two people? Person 1 does A (0 to 2), C (2 to 4), E (4 to 7). Person 2 does B (0 to 3), then D (3 to 7), because D needs A, which finished at hour 2. E starts at hour 4 and needs B (done at 3) and C (done at 4), so it can. Everything finishes at hour 7. Also total work 14 divided by 2 workers is 7, which agrees. **One person: 14 hours. Two people: 7 hours.**

**Q16** 🟡 Budget is later than Audit (clue 2) and later than Launch (clue 4). Hiring is before Audit (clue 1: Audit starts one hour after Hiring), so Hiring is also before Budget. Budget is later than the other three, so Budget is in the last slot, 12. Launch and Budget are in consecutive slots (clue 3), so Launch is at 11. Hiring and Audit take 9 and 10 with Audit one hour after Hiring: Hiring 9, Audit 10. All clues check. **Launch starts at 11.**

**Q17** 🟡 Ravi is not on Afternoon or Night (clues 1, 2), so Ravi is on Morning or Evening. Tej is also not on Afternoon or Night (clues 3, 4), so Tej is on Morning or Evening. Ravi and Tej therefore fill Morning and Evening between them, and Sana and Uma fill Afternoon and Night between them. Now use the "if" clues.
- Suppose Ravi is on Morning. Clue 5 says Sana is on Night, then clue 6 says Uma is on Evening. But Evening belongs to Tej in this case (Ravi has Morning). Contradiction. So Ravi is not on Morning.
- Ravi is on Evening and Tej is on Morning.
- Sana and Uma share Afternoon and Night. If Sana were on Night, clue 6 would put Uma on Evening, which is Ravi's. Contradiction. So Sana is on Afternoon and Uma is on Night.
Check: clue 5 is "if Ravi is on Morning": Ravi is not, so it asks for nothing. Clue 6 is "if Sana is on Night": Sana is not, so it asks for nothing. **Tej Morning, Sana Afternoon, Ravi Evening, Uma Night.**

**Q18** 🟡 Bhanu can do only Invoice, so Bhanu does Invoice. Remove Invoice from everyone else's options: Asha is left with only Filing, so Asha does Filing. Remove Filing: Chitra has Calls or Email, Dev has only Calls (Invoice is taken), so Dev does Calls. That leaves Email for Chitra. Check: each person has a task they can do and all four tasks are used. **Chitra does Email. Asha: Filing. Bhanu: Invoice. Dev: Calls.**

**Q19** 🔴 Work with HR at floor h. Stores is exactly two floors above HR (clue 1), so Stores is on h+2. Sales is adjacent to HR (clue 4), so Sales is on h+1 or h-1. Accounts is higher than Sales (clue 5). Legal is adjacent to Accounts (clue 2). IT is higher than Legal but not adjacent (clues 3 and 6), so IT is at least two floors above Legal.
- Case Sales on h+1: HR, Sales, Stores are floors h, h+1, h+2.
  - h = 1: floors 4, 5, 6 are left for Accounts, Legal, IT. IT is at least two above Legal, so Legal 4, IT 6, Accounts 5. Accounts (5) is above Sales (2), and Legal (4) is adjacent to Accounts (5). Works.
  - h = 2: block on floors 2 to 4, floors 1, 5, 6 left. Accounts must be above Sales (3), so 5 or 6, and Legal must be adjacent. Accounts 5 gives Legal 4 or 6 (4 is taken, 6 leaves IT on floor 1, not above Legal). Accounts 6 gives Legal 5, and IT has only floor 1. Fails.
  - h = 3: block on 3 to 5, floors 1, 2, 6 left. Accounts above Sales (4) must be floor 6, but then Legal must be on floor 5, which is taken. Fails.
  - h = 4 would need Stores on floor 6 and Sales on floor 5, leaving floors 1 to 3 for Accounts, Legal and IT with Accounts above Sales (5): impossible.
- Case Sales on h-1 (floors h-1, h, and h+2 used): h = 2, 3 or 4.
  - h = 2: Sales 1, HR 2, Stores 4; floors 3, 5, 6 left. Legal and Accounts must be adjacent: 5 and 6 only, leaving IT on floor 3, below them. Fails (IT must be above Legal).
  - h = 3: Sales 2, HR 3, Stores 5; floors 1, 4, 6 left. No two are adjacent, so Legal and Accounts cannot be adjacent. Fails.
  - h = 4: Sales 3, HR 4, Stores 6; floors 1, 2, 5 left. Accounts must be above Sales (floor 3), so floor 5, but then Legal would need floor 4 or 6, both taken. Fails.
Only one case works: HR 1, Sales 2, Stores 3, Legal 4, Accounts 5, IT 6. **Floor 1: HR. Floor 4: Legal.**

**Q20** 🔴 The blue box holds the mugs (clue 6). The yellow box is next to the mugs box, so next to blue (clue 4). The badges box is next to yellow (clue 5) and cannot be the blue box (blue holds mugs), so the badges box is on the other side of yellow. So three in a row: either blue, yellow, badges-box, or badges-box, yellow, blue.
- Order badges-box, yellow, blue: blue is somewhere left of red (clue 7), so red is right of blue, which means blue is at 3 and red at 4. Red is immediately left of the Delhi box (clue 2), but nothing is right of position 4. Also blue at 2 is not possible here. Fails.
- Order blue, yellow, badges-box: blue at 1 gives yellow 2 and badges-box 3; blue at 2 gives yellow 3 and badges-box 4. In the second case red can only be at position 4 or 1, and blue must be left of red, so red is at 4, which again cannot be left of Delhi. Fails. So blue 1, yellow 2, badges-box 3.
- Red is right of blue and must have a box to its right, so red is at 3 (the badges box) and green is at 4. Items: mugs 1, badges 3, so files and cables go to positions 2 and 4. Clue 3: the files box is immediately left of the Pune box, so files cannot be at 4; files are at 2 and cables at 4. Pune is position 3. Files go to Kochi (clue 1), so position 2 is Kochi. Red (3) is immediately left of Delhi, so Delhi is position 4. Goa is position 1.
Final: 1 blue mugs Goa, 2 yellow files Kochi, 3 red badges Pune, 4 green cables Delhi. **The green box goes to Delhi, and it holds the cables.**

**Q21** 🔴 The year is not a leap year, so February has 28 days. A 31-day month moves the same date forward 3 weekdays, a 30-day month 2, and February (28 days) 0. Moving the 13th from month to month, with February's 13th as offset 0 (offset = how many weekdays after February's 13th):
- February 0. March 0 (February has 28 days, shift 0). April 3 (March has 31 days). May 5 (April has 30 days, shift 2). June 1 (May has 31 days: 5 + 3 = 8, which is 1 after removing a full week). July 3 (June, shift 2). August 6 (July, shift 3). September 2 (August: 6 + 3 = 9, minus 7). October 4 (September, shift 2). November 0 (October: 4 + 3 = 7, which is 0). December 2 (November, shift 2).
- January is the month before February and has 31 days, so January's 13th is 3 weekdays before February's: offset -3, the same as +4.
Offsets by month: Jan 4, Feb 0, Mar 0, Apr 3, May 5, Jun 1, Jul 3, Aug 6, Sep 2, Oct 4, Nov 0, Dec 2. Months with the same offset share a weekday for their 13th. The offset 6 belongs to August alone. So "August is the only month with a Friday 13th" means August's 13th is a Friday and no other offset class is Friday, which fits: offset 6 is the only class with a single month.
- February's 13th is 6 weekdays before August's Friday, which is Saturday. January's 13th (offset 4) is 4 weekdays after that Saturday: Sunday, Monday, Tuesday, Wednesday. So 13 January is a Wednesday. 1 January is 12 days earlier; 12 days is 1 week plus 5, so go back 5 weekdays from Wednesday: Tuesday, Monday, Sunday, Saturday, Friday. **1 January is a Friday.**
- December's 13th has offset 2, so 2 weekdays after Saturday: Monday. 25 December is 12 days later, which is 1 week plus 5, so Monday plus 5: Tuesday, Wednesday, Thursday, Friday, Saturday. **25 December is a Saturday.**
Cross-check: a date library confirms that every non-leap year whose only Friday 13th is in August starts on a Friday and has 25 December on a Saturday (and that such a year exists, for example 1909).

**Q22** 🔴 Total work is 2 + 4 + 3 + 2 + 5 + 3 = 19 hours. Waiting chains: A then C then F is 2 + 3 + 3 = 8; A then D then F is 2 + 2 + 3 = 7; B then E is 4 + 5 = 9. The critical path is 9 hours, so no number of people can beat 9.
- **Three people: 9 hours.** Person 1: B (0 to 4), E (4 to 9). Person 2: A (0 to 2), C (2 to 5), F (5 to 8) (F needs C at hour 5 and D at hour 4). Person 3: D (2 to 4), after A has finished at hour 2. Everything is done by hour 9. This matches the critical path, so it is the best possible.
- **Two people: 10 hours.** Lower bound: 19 hours of work shared by 2 people is 9.5, so at least 10 hours. 10 is reachable: Person 1 does B (0 to 4), E (4 to 9). Person 2 does A (0 to 2), C (2 to 5), D (5 to 7), F (7 to 10); F needs C and D, both done by hour 7. Finish at hour 10. Brute force over all task orders and assignments confirms 9 is impossible with two people.
**Two people: 10 hours. Three people: 9 hours.** (A fourth person would not help: still 9.)

**Q23** 🔴 Clue 3 says Bala does not do Payroll, Training, Onboarding or Reports. Of the five tasks only Hiring is left, so **Bala does Hiring**. Clue 2 says if Bala does Hiring then Asha does Payroll, so Asha does Payroll. Clue 1 says if Asha does Payroll then Esha does Training, so Esha does Training. That leaves Onboarding and Reports for Chitra and Dev. Clue 4 says Dev does not do Onboarding, so Dev does Reports and Chitra does Onboarding. Check all four clues. They hold. **Dev does Reports. Chitra does Onboarding.**

**Q24** 🔴 Short names: A = Anil, B = Bina, C = Charu, D = Dilip, E = Esha. Days Monday to Saturday are 1 to 6, with one empty day (gap, G).
- Clue 6: Dilip is right after Anil, so A then D form a block X. Clue 3: Bina is right after Esha, so E then B form a block Y.
- Clue 1 (Anil and Bina not consecutive): in the order Y then X, Bina would be directly next to Anil, which is forbidden. Clue 2 (Esha and Dilip not consecutive): in the order X then Y, Dilip would be directly next to Esha, which is forbidden. So X and Y can never touch; a gap or Charu must separate them.
- Clue 4: Charu is earlier than Dilip, so Charu is before block X. Clue 5 forbids Charu directly before Anil, so Charu is not immediately before X. Clue 7 forbids Charu directly after Bina, so Charu is not immediately after Y.
- If Charu sat between Y and X, she would be right after Bina or right before Anil. Both forbidden. So the separator between Y and X, or X and Y, must be the gap G, and it cannot be Charu.
- If Y comes before X, the order is Y, G, X with Charu somewhere before X. Charu cannot go between Y and X, cannot go after X (she must be before Dilip), and cannot go directly after Y. So she goes first: C, Y, G, X.
- If X comes before Y, Charu is before X, and G must separate X and Y: C, X, G, Y puts Charu right before Anil (forbidden); G, C, X, Y has no separator between X and Y. Neither works.
So the only schedule is C, E, B, G, A, D: Monday Charu, Tuesday Esha, Wednesday Bina, Thursday no delivery, Friday Anil, Saturday Dilip. Check all seven clues: Anil (5) and Bina (3) not consecutive; Esha (2) and Dilip (6) not consecutive; Bina (3) is right after Esha (2); Dilip (6) is later than Charu (1); Anil (5) and Charu (1) not consecutive; Dilip (6) is right after Anil (5); Charu (1) and Bina (3) not consecutive. **No delivery on Thursday; Bina is served on Wednesday.**

**Q25** 🔴 Clue 3: A + C = E. The two smallest different weights add to 1 + 2 = 3, so E is at least 3. Try each value of E.
- E = 3: A and C are 1 and 2, so B and D are 4 and 5. Clue 2 needs A + E > B + C. A + E is at most 2 + 3 = 5, but B + C is at least 4 + 1 = 5. Not strictly greater. Fails.
- E = 5: A and C are {1, 4} or {2, 3}, so B and D are the other two. Clue 1 needs B + D > C + E. Either way B + D is 5 (when {A, C} = {1, 4}, B and D are 2 and 3) or 5 (when {A, C} = {2, 3}, B and D are 1 and 4), but C + E is at least 6. Fails.
- E = 4: A and C are 1 and 3, so B and D are 2 and 5. Clue 1: B + D = 7 must beat C + 4, so C is 1 (not 3), so A is 3. Clue 4: B + 4 > 3 + D. If B = 2 and D = 5: 6 > 8 is false. If B = 5 and D = 2: 9 > 5 is true. So B = 5, D = 2.
Result: A = 3, B = 5, C = 1, D = 2, E = 4. Check: B + D = 7 > C + E = 5; A + E = 7 > B + C = 6; A + C = 4 = E; B + E = 9 > A + D = 5. All hold, and no other assignment survives. **Box E weighs 4 kg.**

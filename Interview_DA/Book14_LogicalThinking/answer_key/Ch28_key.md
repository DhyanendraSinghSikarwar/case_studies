# Chapter 28 Answer Key

## Self-check answers

1. Understand, Plan, Execute, Review.
2. Step 1 (Understand) should have caught it. It asks "what exactly is the unknown, and what are the units?" The meeting lasts 2 hours = 120 minutes, minus a 10-minute break gives 110 minutes of talking. The answer "2" was in hours and ignored the break.
3. Step 4 (Review): check fit, reasonableness, and a second route.

---

## Practice answers (each shown in the four steps)

### Q1 🟢 Notebook price

- **Understand:** unknown = notebook price. Givens: 4 notebooks + 3 pens = 290; pen = 30.
- **Plan:** find the pens' cost, subtract from the total, divide by 4.
- **Execute:** 3 pens = 3 x 30 = 90. Notebooks cost 290 - 90 = 200. One notebook = 200 / 4 = 50.
- **Review:** 4 x 50 = 200, plus 90 = 290. Correct.

**Answer: 50 rupees.**

### Q2 🟢 Canteen shifts

- **Understand:** unknown = end time of the last shift. 4 shifts of 35 minutes; gaps only between shifts, so 3 gaps of 5 minutes.
- **Plan:** total minutes, then add to 11:45.
- **Execute:** shifts 4 x 35 = 140; gaps 3 x 5 = 15; total 155 minutes = 2 h 35 min. 11:45 + 2 h = 13:45; + 35 min = 14:20.
- **Review:** list: 11:45 to 12:20, gap to 12:25, 12:25 to 13:00, gap to 13:05, 13:05 to 13:40, gap to 13:45, 13:45 to 14:20. Matches. (Using 4 gaps would give 14:25, wrong.)

**Answer: 14:20.**

### Q3 🟢 Parcels

- **Understand:** unknown = second heaviest. Clues: P > Q, R < Q, S > P (heavier).
- **Plan:** chain the clues into one line.
- **Execute:** S > P (clue 3), P > Q (clue 1), Q > R (clue 2). Order from heaviest: S, P, Q, R.
- **Review:** each clue holds in the line. Second in line is P.

**Answer: P.**

### Q4 🟡 Pens

- **Understand:** maximise pens with at most 100 rupees. Pack: 5 pens for 40; single: 1 pen for 9. Packs are cheaper per pen (8 versus 9).
- **Plan:** casework on the number of packs (0, 1, 2; three packs cost 120, too much), then spend the rest on singles.
- **Execute:**
  - 0 packs: 100 / 9 gives 11 singles (99 rupees), 11 pens.
  - 1 pack (40): 60 left, 60 / 9 gives 6 whole singles (54 rupees), so pens = 5 + 6 = 11.
  - 2 packs (80): 20 left, 2 singles (18), pens = 10 + 2 = 12, spending 98.
- **Review:** 12 beats 11. Could 13 be possible? 13 pens with 2 packs would need 3 singles: 80 + 27 = 107 > 100. With 1 pack, 8 singles: 40 + 72 = 112. With 0 packs, 13 singles: 117. No. So 12 is the greatest.

**Answer: 12 pens, using 2 packs and 2 single pens (98 rupees).**

### Q5 🟡 Presenters

- **Understand:** match 3 people to 3 days, all different.
- **Plan:** table and eliminate.
- **Execute:** Ravi is not Monday, not Tuesday, so Ravi is Wednesday. Tom is not Monday, and Wednesday is taken, so Tom is Tuesday. Sana gets Monday (she is not Wednesday, so that is consistent).
- **Review:** Ravi Wed (not Mon/Tue, ok), Sana Mon (not Wed, ok), Tom Tue (not Mon, ok). All different.

**Answer: Sana Monday, Tom Tuesday, Ravi Wednesday.**

### Q6 🟡 Treasurer and secretary

- **Understand:** ordered pairs (treasurer, secretary) of different people from 6, excluding the two pairs that put Ola and Pete together.
- **Plan:** count all, subtract forbidden.
- **Execute:** all pairs 6 x 5 = 30. Forbidden: (Ola, Pete) and (Pete, Ola) = 2. Allowed = 28.
- **Review:** second route by treasurer: Ola has 4 allowed secretaries (not herself, not Pete); Pete has 4; the other four members have 5 each: 4 + 4 + 4 x 5 = 28. Same.

**Answer: 28.**

### Q7 🟡 Two workers, five jobs

- **Understand:** shortest finishing time; durations P3, Q2 (after P), R4, S2 (after R), T1 (after Q and S); two workers.
- **Plan:** find the longest chain of waiting jobs, then try to fit two workers around it.
- **Execute:**
  - Chain through P and Q: P (3) then Q (2) = 5 hours.
  - Chain through R and S: R (4) then S (2) = 6 hours.
  - T needs both chains finished, so T starts at hour 6 at the earliest and ends at hour 7.
  - Plan: worker 1 does P then Q (hours 0 to 5), then waits; worker 2 does R then S (0 to 6); T by either worker from 6 to 7.
- **Review:** the chain R, S, T is 4 + 2 + 1 = 7 hours and must run in sequence, so nothing shorter is possible. Brute force over all orders and worker assignments confirms 7.

**Answer: 7 hours.**

### Q8 🔴 Tickets

- **Understand:** let a = 50-rupee tickets, b = 30-rupee, c = 20-rupee. a + b + c = 10; 50a + 30b + 20c = 320; a = b.
- **Plan:** use a = b to remove one unknown, then use the ticket count to remove another.
- **Execute:** with b = a: 2a + c = 10, so c = 10 - 2a. Money: 50a + 30a + 20(10 - 2a) = 320, so 80a + 200 - 40a = 320, so 40a = 120, so a = 3. Then b = 3 and c = 4.
- **Review:** 3 + 3 + 4 = 10 tickets; 150 + 90 + 80 = 320. Correct. (Brute force over all splits of 10 tickets: only 3, 3, 4 satisfies all conditions.)

**Answer: three 50-rupee, three 30-rupee, four 20-rupee tickets.**

### Q9 🔴 Lock code

- **Understand:** digits H, T, U, all different, H + T + U = 12, H = 2U, T > H, code odd (so U is odd).
- **Plan:** list possible U (odd digits, since H = 2U must be a digit up to 9), then test.
- **Execute:** U must be odd and 2U at most 9, so U is 1, 3 (U = 5 would make H = 10, not a digit).
  - U = 1: H = 2, T = 12 - 2 - 1 = 9. T = 9 > 2 yes. Digits 2, 9, 1 are different. Code 291.
  - U = 3: H = 6, T = 12 - 6 - 3 = 3. T equals U, digits not different (and 3 is not above 6). Fails.
- **Review:** 2 + 9 + 1 = 12; 2 = 2 x 1; 9 > 2; 291 is odd. Without the "odd" clue, 462 would also fit (U = 2, H = 4 = 2 x 2, T = 6, and 4 + 6 + 2 = 12, 6 > 4), so the "odd" clue is what makes the code unique.

**Answer: 291.**

### Q10 🔴 Floors and drinks

- **Understand:** 4 people, floors 1 to 4 (all different), drinks all different. Six clues.
- **Plan:** place the firm facts first (Jon floor 4, coffee on floor 1), then use the rest.
- **Execute:**
  1. Jon is on floor 4. The coffee drinker is on floor 1.
  2. Lea drinks neither tea nor coffee, and not juice, so Lea drinks water.
  3. Kai is below Lea, so Lea is not on floor 1 and Lea is not floor 4 (Jon). Lea is on floor 2 or 3; Kai is on a lower floor.
  4. Lea (water) is not the coffee drinker, so the coffee drinker is on floor 1 and is not Lea. If Lea were on floor 2, Kai would be on floor 1 (the only floor below). Then Kai drinks coffee, and the tea drinker is directly above Kai, on floor 2, which is Lea, but Lea drinks water. Contradiction. So Lea is on floor 3.
  5. Kai is below Lea: floor 1 or 2. Ira takes the remaining floor. Floors left for Ira and Kai: 1 and 2.
  6. The tea drinker is directly above Kai. If Kai is on floor 2, tea would be on floor 3 (Lea, water). Contradiction. So Kai is on floor 1 and Ira on floor 2. Kai is on floor 1, so Kai drinks coffee (the floor 1 drinker). The tea drinker is on floor 2: Ira.
  7. Remaining drink: juice goes to Jon.
- **Review:** tea (Ira, floor 2) is directly above Kai (floor 1). Jon is on 4. Lea drinks water (not tea, coffee or juice). Coffee drinker (Kai) is on floor 1. Kai (1) is below Lea (3). Brute force over all 576 assignments confirms this is the only solution.

**Answer: Kai floor 1 coffee, Ira floor 2 tea, Lea floor 3 water, Jon floor 4 juice.**
